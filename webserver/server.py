# Flask imports
from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
import os
from webserver.gui_utils import guiAgent, guiEnv, guiState, read_init, serialize
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import json

# Fix payload issue
from engineio.payload import Payload
Payload.max_decode_packets = 50

# Start up Flask web env
template_dir = os.path.abspath('webserver/old_html/')
app = Flask(__name__, template_folder=template_dir)


socketio = SocketIO(app,cors_allowed_origins="*")
fifo_out = 'webserver/webserver.out'
fifo_in = 'webserver/webserver.in'
out = open(fifo_out, "wb")
inp = open(fifo_in, "rb")
print("Webserver In Has")
print(inp.readlines())

# Read initial positions of agents and info about the environment
agent_list, env_info = None, None
while not agent_list or not env_info:
    print("READING THE INIT")
    agent_list, env_info = read_init(inp)

print(f"FINISHED INIT with \n Agents: {agent_list} \n Env Info: {env_info}")


# Home page for website, has all information we want on it
@app.route("/agents")
def agents():
    global agent_list, env_info
    update_sim_info()
    al_string = json.dumps(agent_list)
    return al_string

@app.route("/envInfo")
def envInfo():
    global env_info
    update_sim_info()
    envInfo_string = json.dumps(env_info)
    return envInfo_string


@app.route("/mapImage")
def mapImage():
    return send_file("images/empty_map.jpg", mimetype='image/jpeg')

@app.route("/mapImageBackground")
def mapImageBackground():
    return send_file("images/empty_map_background.jpg", mimetype='image/jpeg')

@app.route("/renderedScene")
def renderedScene():
    return send_file("images/rendered_scene.jpg", mimetype='image/jpeg')

# Home page for website, has all information we want on it
@app.route("/")
def index():
    return render_template("agents.html", agent_list=agent_list, env_info=env_info)

# Update the simulator info
@socketio.on("update_sim_info")
def update_sim_info():
    global agent_list, env_info
    new_agent_list, new_env_info = read_init(inp)
    if new_agent_list:
        agent_list = new_agent_list
    if new_env_info:
        env_info = new_env_info


# On socket update change agent angle
@socketio.on("agent_angle")
def agent_angle(data):
    global out
    a_id = str(data['id'])
    angle = int(data['value'])
    agent_change = guiAgent(change="angle", agent_id=a_id, cur_angle=angle)
    print(f"Sending Agent {a_id} angle {angle}")
    serialize(agent_change, out)
 
# On socket update change agent angle position (from text)
@socketio.on("agent_pos")
def agent_pos(data):
    global out
    a_id = str(data['id'])
    x = data['x']
    z = data['z']
    agent_change = guiAgent(change="pos", agent_id=a_id, cur_pos=[x, 0, z])
    print(f"Sending Agent {a_id} pos {(x, z)}")
    serialize(agent_change, out)

# On socket update change agent angle position (from button press)
@socketio.on("increment_pos")
def increment_pos(data):
    global out
    a_id = str(data['id'])
    direction = str(data['direction'])
    agent_change = guiAgent(change="inc_pos", agent_id=a_id, inc_direction=direction)
    serialize(agent_change, out)

@socketio.on("lights")
def lights(data):
    global oute
    a_id = str(data['id'])
    lights = data['lights']
    agent_change = guiAgent(change="lights", agent_id=a_id, lights=lights)
    print(f"Sending Agent {a_id} lights {lights}")
    serialize(agent_change, out)
 
# On socket update resume simulation from button press
@socketio.on("sim_state")
def sim_state(data):
    global out
    state = str(data['state'])
    to_send = guiState(state=state)
    print(f"Sending state {state}")
    serialize(to_send, out)

@socketio.on("delete_agent")
def delete_agent(data):
    global out
    a_id = str(data['id'])
    to_send = guiAgent(change="delete", agent_id=a_id)
    print(f"Sending Agent {a_id} delete")
    serialize(to_send, out)

@socketio.on("add_agent")
def add_agent():
    global out
    to_send = guiAgent(change="add")
    print(f"Sending Agent add")
    serialize(to_send, out)

@socketio.on("turn_choice")
def turn_choice(data):
    global out
    a_id = str(data['agent_id'])
    turn = str(data['turn'])
    if turn == "Random":
        turn = None
    to_send = guiAgent(change="turn", agent_id=a_id, turn_choice=turn)
    print(f"Setting Turn to {turn} for agent {a_id}")
    serialize(to_send, out)

if __name__ == '__main__':
    socketio.run(app)
