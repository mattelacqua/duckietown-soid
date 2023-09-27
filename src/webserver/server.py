# Flask imports
from flask import Flask, send_file
from flask_socketio import SocketIO
import os
from webserver.gui_utils import read_init, serialize, unserialize
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import json
from flask_cors import CORS, cross_origin

# Fix payload issue
from engineio.payload import Payload
Payload.max_decode_packets = 100

# Start up Flask web env
template_dir = os.path.abspath('src/webserver/old_html/')
app = Flask(__name__, template_folder=template_dir)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# start a socket
socketio = SocketIO(app,cors_allowed_origins="*")

# Open the pipes for backend -> frontend coms
fifo_out = 'src/webserver/webserver.out'
fifo_in = 'src/webserver/webserver.in'
fifo_log = 'src/webserver/webserver.log'
out = open(fifo_out, "w")
inp = open(fifo_in, "r")
logger = open(fifo_log, "r")

# Read initial positions of agents and info about the environment
env_info = None
log_info = []
while not env_info:
    env_info = read_init(inp)

# Home page for website, has all information we want on it
@app.route("/envInfo.json")
@cross_origin()
def envInfo():
    global env_info
    update_sim_info()
    envInfo_string = json.dumps(env_info)
    return envInfo_string

@app.route("/mapImage")
@cross_origin()
def mapImage():
    return send_file("images/empty_map.jpg", mimetype='image/jpeg')

@app.route("/mapImageBackground")
@cross_origin()
def mapImageBackground():
    return send_file("images/empty_map_background.jpg", mimetype='image/jpeg')

@app.route("/renderedScene")
@cross_origin()
def renderedScene():
    return send_file("images/rendered_scene.jpg", mimetype='image/jpeg')

#Connect and Disconnect
@socketio.on('connect')
def test_connect(auth):
    print(f"New Socket Client Connection: {auth}")

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# Update the simulator info
@socketio.on("update_sim_info")
def update_sim_info():
    global env_info
    new_env_info = read_init(inp)
    if new_env_info:
        env_info = new_env_info

# On socket update change agent angle
@socketio.on("agent_angle")
def agent_angle(data):
    global out
    a_id = str(data['id'])
    angle = int(data['value'])
    agent_change = {
                    'kind': 'change',
                    'change': 'angle',
                    'agent_id': a_id,
                    'cur_angle': angle,
                    }

    serialize(agent_change, out)
 
# On socket update change agent angle
@socketio.on("initial_direction")
def initial_direction(data):
    global out
    a_id = int(data['agent_index'])
    initial_direction = str(data['initial_direction'])
    agent_change = {
                    'kind': 'change',
                    'change': 'initial_direction',
                    'agent_id': a_id,
                    'initial_direction': initial_direction,
                    }
    serialize(agent_change, out)

# On socket update change agent angle
@socketio.on("intersection_arrival")
def intersection_arrival(data):
    global out
    a_id = int(data['agent_index'])
    intersection_arrival = int(data['intersection_arrival'])
    agent_change = {
                    'kind': 'change',
                    'change': 'intersection_arrival',
                    'agent_id': a_id,
                    'intersection_arrival': intersection_arrival,
                    }
    serialize(agent_change, out)

# On socket update change agent angle position (from map)
@socketio.on("agent_pos")
def agent_pos(data):
    global out
    a_id = str(data['id'])
    x = data['x']
    z = data['z']
    agent_change = {
                    'kind': 'change',
                    'change': 'pos',
                    'agent_id': a_id,
                    'pos_x': x,
                    'pos_z': z,
                    }   
    serialize(agent_change, out)

# On socket update resume simulation from button press
@socketio.on("sim_state")
def sim_state(data):
    global out
    state = str(data['state'])
    to_send = {
                'kind': 'state',
                'state': state,
              }
    print(f"GETTING THE {state}")
    serialize(to_send, out)

# add an agent
@socketio.on("add_agent")
def add_agent():
    global out
    agent_change = {
                    'kind': 'add_agent',
                   }
    serialize(agent_change, out)

# delete an agent
@socketio.on("delete_agent")
def delete_agent(data):
    global out
    a_id = str(data['id'])
    agent_change = {
                    'kind': 'change',
                    'change': 'delete',
                    'agent_id': a_id,
                    }
    serialize(agent_change, out)

@socketio.on("model_choice")
def model_choice(data):
    choice = data['choice']
    counterfactual_wrap = {
        'kind': 'change',
        'change': 'model_choice',
        'choice': choice,
        'agent_id': 0,
    }
    serialize(counterfactual_wrap, out)


# Reinstate from log
@socketio.on("log_step")
def log_step(data):
    global logger, env_info, log_info

    step = int(data['step'])
    new_log_info = list(unserialize(logger, log=True))
    if new_log_info:
        log_info = new_log_info

    # Get it if it exists
    try: log_step = log_info[step]
    except: return ""

    print(f"Log step {json.dumps(log_step, indent=2)}")
    log_change = {
                'kind': 'log',
                'change': 'log',
                'log': log_step
    }
    print(f"Sending out a log change")
    serialize(log_change, out)

# Do a soid query
@socketio.on("query")
def query(query_info):
    query_blob = {
                    'kind': 'query',
                    'query_info': query_info\
                }
    serialize(query_blob, out)

# Add a counterfactual to agent list
@socketio.on("add_counterfactual")
def add_counterfactual(data):
    counterfactual = data['counterfactual']
    
    # filter for turn choices
    turnchoices = []
    for choice in counterfactual['range']['turn_choices']:
        if choice['selected']:
            turnchoices.append(choice['direction'])
    counterfactual['range']['turn_choices'] = turnchoices

    counterfactual_wrap = {
        'kind': 'counterfactual',
        'change': 'add',
        'agent_id': data['index'],
        'counterfactual': counterfactual,
    }
    serialize(counterfactual_wrap, out)

# Delete a counterfactual from agent list
@socketio.on("delete_counterfactual")
def delete_counterfactual(data):
    counterfactual_wrap = {
        'kind': 'counterfactual',
        'change': 'delete',
        'index': data['index'],
        'agent_index': data['agent_index'],
    }
    serialize(counterfactual_wrap, out)


if __name__ == '__main__':
    socketio.run(app, port=5001)

