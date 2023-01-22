# Flask imports
from flask import Flask, render_template, send_file
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


socketio = SocketIO(app,cors_allowed_origins="*")
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

#print(f"FINISHED INIT with \n Agents: {agent_list} \n Env Info: {env_info}")



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
    counterfactual = data['counterfactual']
    agent_change = {
                    'kind': 'change',
                    'change': 'angle',
                    'agent_id': a_id,
                    'cur_angle': angle,
                    'counterfactual': counterfactual
                    }

    #print(f"Sending Agent {a_id} angle {angle}")
    serialize(agent_change, out)
 
# On socket update change agent angle position (from text)
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
    #print(f"Sending Agent {a_id} pos {(x, z)}")
    serialize(agent_change, out)

# On socket update change agent angle position (from button press)
@socketio.on("increment_pos")
def increment_pos(data):
    global out
    a_id = str(data['id'])
    direction = str(data['direction'])
    agent_change = {
                    'kind': 'change',
                    'change': 'inc_pos',
                    'agent_id': a_id,
                    'inc_dir': direction
                    }
    serialize(agent_change, out)

@socketio.on("lights")
def lights(data):
    global oute
    a_id = str(data['id'])
    lights = data['lights']
    agent_change = {
                    'kind': 'change',
                    'change': 'lights',
                    'agent_id': a_id,
                    'lights': lights
                    }
    #print(f"Sending Agent {a_id} lights {lights}")
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
    #print(f"Sending state {state}")
    serialize(to_send, out)

@socketio.on("delete_agent")
def delete_agent(data):
    global out
    a_id = str(data['id'])
    #print(f"Sending Agent {a_id} delete")
    agent_change = {
                    'kind': 'change',
                    'change': 'delete',
                    'agent_id': a_id,
                    }
    serialize(agent_change, out)

@socketio.on("add_agent")
def add_agent():
    global out
    agent_change = {
                    'kind': 'change',
                    'change': 'add',
                    }
    #print(f"Sending Agent add")
    serialize(agent_change, out)

@socketio.on("turn_choice")
def turn_choice(data):
    global out
    a_id = str(data['agent_id'])
    turn = str(data['turn'])
    if turn == "Random":
        turn = None
    agent_change = {
                    'kind': 'change',
                    'change': 'turn',
                    'agent_id': a_id,
                    'turn_choice': turn,
                    }
    print(f"Setting Turn to {turn} for agent {a_id}")
    serialize(agent_change, out)

@socketio.on("signal_choice")
def signal_choice(data):
    global out
    a_id = str(data['agent_id'])
    signal = str(data['signal'])
    if signal == "Random":
        signal = None
    agent_change = {
                    'kind': 'change',
                    'change': 'signal',
                    'agent_id': a_id,
                    'signal_choice': signal,
                    }
    print(f"Setting Signal to {signal} for agent {a_id}")
    serialize(agent_change, out)

# On socket update change agent forward step (use minimum by default 
@socketio.on("forward_step")
def forward_step(data):
    global out
    a_id = str(data['id'])
    forward_step = dict(data['forward_step'])
    # Default to MIN
    agent_change = {
                    'kind': 'change',
                    'change': 'forward_step',
                    'agent_id': a_id,
                    'forward_step': round(forward_step['min'], 2),
                    }
    #print(f"Sending Agent {a_id} forward_step min {forward_step}")
    serialize(agent_change, out)

@socketio.on("bounding_box")
def bounding_box(data):
    global out
    a_id = str(data['id'])
    direction = str(data['direction'])
    bbox_offset = float(data['bbox_offset'])
    print(f"bbox {direction} offset {bbox_offset}")
    if direction == "width":
        agent_change = {
                        'kind': 'change',
                        'change': 'bbox_offset_w',
                        'agent_id': a_id,
                        'bbox_offset_w': round(bbox_offset, 2),
                        }
    elif direction == "length":
        agent_change = {
                        'kind': 'change',
                        'change': 'bbox_offset_l',
                        'agent_id': a_id,
                        'bbox_offset_l': round(bbox_offset, 2),
                        }
    #print(f"Sending Agent {a_id} bbox_offset {bbox_offset} direction {direction}")
    serialize(agent_change, out)

@socketio.on("log_step")
def log_step(data):
    global logger, agent_list, env_info, log_info
    step = int(data['step'])
    new_log_info = list(unserialize(logger, log=True))
    if new_log_info:
        log_info = new_log_info

    # Get the closest step possible
    if step != 0:
        step = int(round(step / 10))

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

@socketio.on("query")
def query(query_info):

    query_blob = {
                    'kind': 'query',
                    'query_info': query_info\
                }
    serialize(query_blob, out)
                  
    

if __name__ == '__main__':
    socketio.run(app, port=5001)

