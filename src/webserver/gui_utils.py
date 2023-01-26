from gym_duckietown import agents, simulator, objects, logger
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
import numpy as np
import math
import pickle
import json
import subprocess
import os
import signal
import time
from webserver import counterfactual as cf

def handle_input(env, gui_input):
    # If its a state update
    if gui_input['kind'] == 'state':
        state = gui_input['state']
        env.state = state
        return state


    if gui_input['kind'] == 'change':
        change = gui_input['change']
        agent = env.agents[int(gui_input['agent_id'])]
        if change == "angle":
            agent.cur_angle = math.radians(gui_input['cur_angle'])
            agent.deg_angle = agent.get_curr_angle(env)
            agent.direction = agent.get_direction(env)
        elif change == "pos":
            agent.cur_pos = [gui_input['pos_x'], 0, gui_input['pos_z']]
            agent.actions = []
        elif change == "delete":
            env.agents.remove(agent)
                
    if gui_input['kind'] == 'add_agent':
        new_agent = agents.Agent(env, agent_id=("agent"+str(len(env.agents))), random_spawn=True)
        directions = ['N', 'N',  'S', 'S', 'E', 'E', 'W', 'W']
        colors = ['green', 'red', 'grey', 'cyan', 'yellow', 'orange', 'midnight']
        env.agents.append(new_agent)
        env.spawn_random_agent(new_agent, directions, colors)
         

    if gui_input['kind'] == 'log':
        for agent in env.agents:
            for log_agent in gui_input['log']['agents']:
                if agent.agent_id == log_agent['agent_id']:
                    agent.cur_pos = [log_agent['pos_x'], 0, log_agent['pos_z']]
                    agent.cur_angle = log_agent['angle']
                    agent.color = from_html_color(log_agent['color'])
                    agent.turn_choice = log_agent['turn_choice']
                    agent.signal_choice = log_agent['signal_choice']
                    agent.curve = agent.get_curve(env)
                    agent.speed = log_agent['speed']
                    agent.forward_step = log_agent['forward_step']
                    agent.direction = agent.get_direction(env)
                    agent.intersection_arrival = log_agent['intersection_arrival']
                    agent.patience = log_agent['patience']
                    agent.step_count = log_agent['step_count']
                    agent.lookahead = log_agent['lookahead']
                    agent.states['in_intersection'] = log_agent['state']['in_intersection']
                    agent.states['at_intersection_entry'] = log_agent['state']['at_intersection_entry']
                    agent.states['intersection_empty'] = log_agent['state']['intersection_empty']
                    agent.states['approaching_intersection'] = log_agent['state']['approaching_intersection']
                    agent.states['obj_in_range'] = log_agent['state']['obj_in_range']
                    agent.states['has_right_of_way'] = log_agent['state']['has_right_of_way']
                    agent.states['next_to_go'] = log_agent['state']['next_to_go']
                    agent.states['safe_to_enter'] = log_agent['state']['safe_to_enter']
                    agent.states['cars_waiting_to_enter'] = log_agent['state']['cars_waiting_to_enter']
                    agent.states['car_entering_range'] = log_agent['state']['car_entering_range']
                    agent.states['obj_behind_intersection'] = log_agent['state']['obj_behind_intersection']
                    agent.states['is_tailgating'] = log_agent['state']['is_tailgating']
                    agent.bbox_offset_w = log_agent['bbox_w']
                    agent.bbox_offset_l = log_agent['bbox_l']
                    agent.state = log_agent['state']
                    agent.lights = log_agent['lights']
                    agent.step_count = log_agent['step_count']

                    agent.state = pickle.loads(eval(log_agent['car_state']))
                    agent.counterfactuals = log_agent['counterfactuals']

    
    if gui_input['kind'] == 'query':
        query_blob = cf.get_query_blob(env, gui_input['query_info'])

        print("\n\n Final Query Blob")
        print(json.dumps(query_blob, indent=2))

        klee_file = cf.generate_klee_file(query_blob)
        soid_query = cf.generate_soid_query(query_blob)
        soid_result = cf.invoke_soid(soid_query, klee_file)
        
        
        env.state = 'query_result'
        return env.state, soid_result
        


    env.c_info_struct = agents.EnvironmentInfo(env)
    return env.state, None



# Serialize by pickling to fifo
def serialize(obj, fifo):
    tic = time.perf_counter()
    json.dump(obj, fifo)
    fifo.write('\n')
    fifo.flush()
    toc = time.perf_counter()
    #print("Serialize Time = {0}".format(toc - tic))

# Unserialize from fifo
def unserialize(fifo, log=False):
    tic = time.perf_counter()
    if log:
        lines = fifo.readlines()
        for line in lines:
            line.strip()
            json_line = json.loads(line)
            yield json_line
    else:
        lines = fifo.readlines()
        if lines:
            lines[-1].strip()
            json_line = json.loads(lines[-1])
            yield json_line
        """while True:
            try:
                input = json.load(fifo)
                if input:
                    yield input
            except json.decoder.JSONDecodeError:
                break"""
    
    


# Init agents in server
def init_server(dt, fifo, env, socket, get_map=False):

    tic = time.perf_counter()
    if get_map:
        env.map_jpg(background=True)
        env.map_jpg(background=False)
    
    env_info = env_info_dict(env)
    #print("Data Function Dict Traversal = {0}".format(toc - tic))
    # Serialize the input
    serialize(env_info, fifo)

    if socket:
        socket.emit("update_sim_info")

def env_info_dict(env):
    c_info_struct = env.c_info_struct
    env_info = {}
    env_info['intersection_x'] = int(c_info_struct.intersection_x)
    env_info['intersection_z'] = int(c_info_struct.intersection_z)
    env_info['robot_length'] = float(round(c_info_struct.robot_length, 3))
    env_info['grid_w'] = int(c_info_struct.grid_w)
    env_info['grid_h'] = int(c_info_struct.grid_h)
    env_info['road_tile_size'] = float(round(c_info_struct.road_tile_size, 3))
    env_info['max_steps'] = int(c_info_struct.max_steps)
    env_info['num_agents'] = int(c_info_struct.agents.num_agents)

    agents = []
    for i in range(0, c_info_struct.agents.num_agents):
        agent = c_info_struct.agents.agents_array[i]
        dict_agent = {}
        dict_agent['id'] = int(agent.id)
        dict_agent['pos_x'] = float(round(agent.pos_x, 3))
        dict_agent['pos_z'] = float(round(agent.pos_z, 3))
        dict_agent['prev_pos_x'] = float(round(agent.prev_pos_x, 3))
        dict_agent['prev_pos_z'] = float(round(agent.prev_pos_z, 3))
        dict_agent['stop_x'] = float(round(agent.stop_x, 3))
        dict_agent['stop_z'] = float(round(agent.stop_z, 3))
        dict_agent['tile_x'] = int(agent.tile_x)
        dict_agent['tile_z'] = int(agent.tile_z)
        dict_agent['angle'] = float(round(agent.angle, 3))
        dict_agent['speed'] = float(round(agent.speed, 3))
        dict_agent['forward_step'] = float(round(agent.forward_step, 3))
        dict_agent['direction'] = int(agent.direction)
        dict_agent['intersection_arrival'] = int(agent.intersection_arrival)
        dict_agent['patience'] = int(agent.patience)
        dict_agent['step_count'] = int(agent.step_count)
        dict_agent['lookahead'] = float(round(agent.lookahead, 3))

        agent_state = {}
        agent_state['in_intersection'] = agent.state.in_intersection
        agent_state['at_intersection_entry'] = agent.state.at_intersection_entry
        agent_state['intersection_empty'] = agent.state.intersection_empty
        agent_state['approaching_intersection'] = agent.state.approaching_intersection
        agent_state['obj_in_range'] = agent.state.obj_in_range
        agent_state['has_right_of_way'] = agent.state.has_right_of_way
        agent_state['next_to_go'] = agent.state.next_to_go
        agent_state['safe_to_enter'] = agent.state.safe_to_enter
        agent_state['cars_waiting_to_enter'] = agent.state.cars_waiting_to_enter
        agent_state['car_entering_range'] = agent.state.car_entering_range
        agent_state['obj_behind_intersection'] = agent.state.obj_behind_intersection
        agent_state['is_tailgating'] = agent.state.is_tailgating

        dict_agent['state']=agent_state
        dict_agent['exists']=agent.exists
        
        # Other things not included in c struct
        dict_agent['agent_id'] = env.agents[i].agent_id
        dict_agent['color'] = html_color(env.agents[i].color)
        dict_agent['turn_choice'] = env.agents[i].turn_choice
        dict_agent['signal_choice'] = env.agents[i].signal_choice
        dict_agent['lights'] = env.agents[i].lights
        dict_agent['angle_deg'] = env.agents[i].get_curr_angle(env)
        dict_agent['bbox_w'] = env.agents[i].bbox_offset_w
        dict_agent['bbox_l'] = env.agents[i].bbox_offset_l
        dict_agent['car_state']= str(pickle.dumps(env.agents[i].state))
        dict_agent['counterfactuals'] = env.agents[i].counterfactuals

        agents.append(dict_agent)

    env_info['agents'] = agents
    env_info['state'] = env.state
    env_info['sim_step'] = env.agents[0].step_count

    return env_info
    
    
# Read initial positions and env info
def read_init(fifo, log=False):
    agent_list =[] 
    env_info = {}
    log_list = []
    
    input_list = list(unserialize(fifo, log))

    if log:
        fifo.seek(0)

    if input_list:
        env_info = {}
        for input in input_list:
            print(len(input_list))
            env_info = input
        if log:
            return {'step': env_info['agents'][0]['step_count'],
                    'env_info': env_info}
        else:
            return env_info
    else:
        return None

# Kill old webserver if it exists, otherwise start new subprocess.
def start_webserver():
    cmd = ['pgrep -f .*python.*webserver/server.py']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    my_pid, err = process.communicate()

    if len(my_pid.splitlines()) >0:
       print("Old webserver running. Killing old and starting up new")
       os.kill(int(my_pid.decode("utf-8")), signal.SIGTERM)
    else:
      print("Old webserver not Running, Starting up new")

    webserver = subprocess.Popen(["python","src/webserver/server.py"])
    return webserver

def start_node():
    cmd = ['pgrep -f .*.*start.js']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    print(my_pid)

    if len(my_pid.splitlines()) >0:
       print("Old NJS SCRIPT Running Killing.")
       os.kill(int(my_pid.decode("utf-8")), signal.SIGTERM)
    else:
      print("Old NJS SCRIPT not Running, Starting up new")    
      
    cmd = ['pgrep -f .*npm.*start']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    my_pid, err = process.communicate()

    if len(my_pid.splitlines()) >0:
       print("Old NJS Running Killing.")
       os.kill(int(my_pid.decode("utf-8")), signal.SIGTERM)
    else:
      print("Old NJS not Running, Starting up new")




    node = subprocess.Popen(["npm","start", "--prefix", "src/webserver/web-gui"])
    return node


# Get html color
def html_color(color: str):
    colors = {
        "green": "Green",
        "red": "FireBrick",
        "grey": "DimGray",
        "blue": "DarkBlue",
        "cyan": "Cyan",
        "yellow": "#F5CD00",
        "orange": "Orange",
        "midnight": "Indigo"
    }
    color = colors[color]
    return color

def from_html_color(color: str):
    colors = {
        "Green": "green",
        "FireBrick": "red",
        "DimGray": "grey",
        "DarkBlue": "blue",
        "Cyan": "cyan",
        "#F5CD00": "yellow",
        "Orange": "orange",
        "Indigo": "midnight"
    }
    color = colors[color]
    return color
    
