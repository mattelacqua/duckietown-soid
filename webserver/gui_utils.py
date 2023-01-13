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

# Check if Scene is all set
class guiState():
    state: str

    def __init__(self,
        state = "running"):

        self.state = state

    # If done return this so that in pause of our function we know what to do
    def handle_input(self, env):
        env.state = self.state
        return self.state 

# Store the # of steps we are
class guiSteps():
    step: int

    def __init__(self,
        step = 0):

        self.step = step

    # If we get a step, return it
    def handle_input(self, env):
        return env.state # So it doesn't break. TODO




# Class for any agent changes
# IF ADDING ANYTHING MAKE SU?RE TO ADD IT TO UNSERIALIZE TOO
class guiAgent():
    change: str     # Should be 'angle' 'pos' 'inc_pos' 'inc_speed'
    agent_id: str 
    index: int 
    color: str
    cur_pos: List[float]
    cur_angle: float
    forward_step: float
    inc_direction: str
    lights:  List
    turn_choice: str
    signal_choice: str
    bbox_offset_w: float
    bbox_offset_l: float
    state: None
    learning_state: None
    log_lights: List
    log_pos: List
    log_angle: None
    log_color: None
    
    
    def __init__(self,
        change = "",
        agent_id = "",
        index = -1,
        cur_pos = {},
        cur_angle = -1.0,
        color = "",
        inc_direction = "",
        lights = [],
        turn_choice= None,
        forward_step= 0.0,
        bbox_offset_w= 0.0,
        bbox_offset_l= 0.0,
        state= None,
        learning_state= {},
        signal_choice= None,
        log_lights= None,
        log_pos= None,
        log_angle= None,
        log_color= None,
        ):

        self.change = change
        self.agent_id = agent_id
        self.index = index
        self.color = color
        self.cur_pos = cur_pos
        self.cur_angle = cur_angle
        self.inc_direction = inc_direction
        self.lights = lights
        self.turn_choice = turn_choice
        self.signal_choice = signal_choice
        self.forward_step = forward_step
        self.bbox_offset_w = bbox_offset_w
        self.bbox_offset_l = bbox_offset_l
        self.state = state
        self.learning_state = learning_state
        self.log_lights = log_lights
        self.log_pos = log_pos
        self.log_angle = log_angle
        self.log_color = log_color


    # Handle agent input. Based on the kind of change, do xyz
    def handle_input(self, env):
        agent_id = self.agent_id
        cur_pos = self.cur_pos
        forward_step = self.forward_step
        cur_angle = math.radians(self.cur_angle)
        change = self.change
        lights = self.lights
        color = self.color
        turn_choice = self.turn_choice
        signal_choice = self.signal_choice
        bbox_offset_l = self.bbox_offset_l
        bbox_offset_w = self.bbox_offset_w


        agent_count = 0
        for agent in env.agents:
            if agent.agent_id == agent_id:
                #print("Changing {0}'s current angle from {1} to {2}".format(agent.agent_id, agent.cur_angle, cur_angle))
                if change == "angle":
                    agent.cur_angle = cur_angle
                elif change == "forward_step":
                    agent.forward_step = forward_step
                elif change == "pos":
                    agent.cur_pos = cur_pos
                    #Resetting the actions for the agent since pos change will revert
                    agent.actions = []
                elif change == "inc_pos":
                    if self.inc_direction == 'N':
                        agent.cur_pos[2] -= 0.1
                    elif self.inc_direction == 'S':
                        agent.cur_pos[2] += 0.1
                    elif self.inc_direction == 'E':
                        agent.cur_pos[0] += 0.1
                    elif self.inc_direction == 'W':
                        agent.cur_pos[0] -= 0.1
                elif change == "turn":
                    agent.turn_choice = turn_choice
                elif change == "signal":
                    agent.signal_choice = signal_choice
                elif change == "bbox_offset_w":
                    agent.bbox_offset_w = bbox_offset_w
                elif change == "bbox_offset_l":
                    agent.bbox_offset_l = bbox_offset_l
                elif change == "lights":
                    for light in lights:
                        agent.set_light(light["light"], light["on"])
                elif change == "delete":
                    env.agents.remove(agent)
                
            agent_count = agent_count + 1
        if change == "add":
            new_agent = agents.Agent(agent_id=("agent"+str(agent_count)))
            env.agents.append(new_agent)
         

        # Return false because not done command
        return env.state 
# Send information through guiEnv
class guiEnv():
    max_NS: int
    max_EW: int
    intersection_x: int
    intersection_z: int
    grid_w: int
    grid_h: int
    road_tile_size: int
    max_steps: int
    num_agents: int
    agents: List[guiAgent]
    state: guiState
    map_image: None

    def __init__(self,
        max_NS = 0,
        max_EW = 0,
        intersection_x = 0,
        intersection_z = 0,
        grid_w = 0,
        grid_h = 0,
        road_tile_size = 0,
        max_steps = 0,
        num_agents = 0,
        agents = [],
        state = None,
        map_image = None
        ):

        self.max_NS = max_NS
        self.max_EW = max_EW
        self.intersection_x = intersection_x
        self.intersection_z = intersection_z
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.road_tile_size = road_tile_size
        self.max_steps = max_steps
        self.num_agents = num_agents
        self.agents = agents
        self.state = state
        self.map_image = map_image


# Handle resetting from Log
class guiLog():
    log_agents: List[guiAgent]
    log_steps: int 

    def __init__(self, log_agents=[], log_steps=0):
        self.log_agents = log_agents
        self.log_steps = log_steps

    def handle_input(self, env):
        for agent in env.agents:
            for log_agent in self.log_agents:
                if agent.agent_id == log_agent.agent_id:
                    agent.cur_pos = log_agent.log_pos
                    agent.cur_angle = log_agent.log_angle
                    agent.color = log_agent.log_color
                    agent.turn_choice = log_agent.turn_choice
                    agent.curve = agent.get_curve(env)
                    agent.signal_choice = log_agent.signal_choice
                    agent.forward_step = log_agent.forward_step
                    agent.bbox_offset_w = log_agent.bbox_offset_w
                    agent.bbox_offset_l = log_agent.bbox_offset_l
                    agent.state = log_agent.state
                    agent.lights = log_agent.log_lights
                    agent.step_count = self.log_steps

        return env.state



# Serialize by pickling to fifo
def serialize(obj, fifo):
    tic = time.perf_counter()
    json.dump(obj, fifo)
    print(f"Dumped {obj}")
    fifo.flush()
    toc = time.perf_counter()
    #print("Serialize Time = {0}".format(toc - tic))

# Unserialize from fifo
def unserialize(fifo, log=False):
    tic = time.perf_counter()
    while True:
        try:
            input = json.load(fifo)
            if input:
                print(f"LOADED {input}")
                yield input
        except json.decoder.JSONDecodeError:
            break
    
    


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
    env_info['intersection_x'] = c_info_struct.intersection_x
    env_info['intersection_z'] = c_info_struct.intersection_z
    env_info['robot_length'] = c_info_struct.robot_length
    env_info['grid_w'] = c_info_struct.grid_w
    env_info['grid_h'] = c_info_struct.grid_h
    env_info['road_tile_size'] = c_info_struct.road_tile_size
    env_info['max_steps'] = c_info_struct.max_steps
    env_info['num_agents'] = c_info_struct.agents.num_agents

    agents = []
    for i in range(0, c_info_struct.agents.num_agents):
        agent = c_info_struct.agents.agents_array[i]
        dict_agent = {}
        dict_agent['id'] = agent.id
        dict_agent['pos_x'] = agent.pos_x
        dict_agent['pos_z'] = agent.pos_z
        dict_agent['prev_pos_x'] = agent.prev_pos_x
        dict_agent['prev_pos_z'] = agent.prev_pos_z
        dict_agent['stop_x'] = agent.stop_x
        dict_agent['stop_z'] = agent.stop_z
        dict_agent['tile_x'] = agent.tile_x
        dict_agent['tile_z'] = agent.tile_z
        dict_agent['angle'] = agent.angle
        dict_agent['speed'] = agent.speed
        dict_agent['forward_step'] = agent.forward_step
        dict_agent['direction'] = agent.direction
        dict_agent['intersection_arrival'] = agent.intersection_arrival
        dict_agent['patience'] = agent.patience
        dict_agent['step_count'] = agent.step_count
        dict_agent['lookahead'] = agent.lookahead

        agent_state = {}
        agent_state['in_intersection'] = agent.state.in_intersection
        agent_state['at_intersection_entry'] = agent.state.at_intersection_entry
        agent_state['intersection_empty'] = agent.state.intersection_empty
        agent_state['approaching_intersection'] = agent.state.approaching_intersection
        agent_state['obj_in_range'] = agent.state.obj_in_range
        agent_state['has_right_of_way'] = agent.state.has_right_of_way
        agent_state['cars_waiting_to_enter'] = agent.state.cars_waiting_to_enter
        agent_state['car_entering_range'] = agent.state.car_entering_range
        agent_state['obj_behind_intersection'] = agent.state.obj_behind_intersection
        agent_state['is_tailgating'] = agent.state.is_tailgating
        agent_state['next_to_go'] = agent.state.next_to_go

        dict_agent['state']=agent_state
        dict_agent['exists']=agent.exists
        agents.append(dict_agent)

    env_info['agents'] = agents

    return env_info
    
    
# Read initial positions and env info
def read_init(fifo, log=False):
    agent_list =[] 
    env_info = {}
    log_list = []
    
    input_list = list(unserialize(fifo, log))

    if log:
        print(f"Input list is {input_list}")
        fifo.seek(0)

    if input_list:
        env_info = {}
        for input in input_list:
            env_info = input
        return env_info
    else:
        return None


    # for each input from init server
    id_no = 0
    if input_list:
        for inputs in input_list:

            # Reset to blank
            agent_list = []
            env_info = {} 
            id_no = 0

            for inp in inputs:
                #print("READING INIT INPUT: {0}".format(inp))
                # if agent add relevant info for webserver to have
                if isinstance(inp, guiAgent):
                    gui_agent = inp
                    agent_list.append({
                                        "id" : id_no,
                                        "agent_id" : gui_agent.agent_id,
                                        "cur_pos" : gui_agent.cur_pos,
                                        "cur_angle" : gui_agent.cur_angle,
                                        "color" : gui_agent.color,
                                        "lights" : gui_agent.lights,
                                        "turn_choice" : gui_agent.turn_choice,
                                        "signal_choice" : gui_agent.signal_choice,
                                        "forward_step" : gui_agent.forward_step,
                                        "bbox_w" : gui_agent.bbox_offset_w,
                                        "bbox_l" : gui_agent.bbox_offset_l,
                                        })
                    id_no += 1

                # if env_info add relevant info for webserver to have
                if isinstance(inp, guiEnv):
                    gui_env = inp
                    env_info["max_NS"] = gui_env.max_NS
                    env_info["max_EW"] = gui_env.max_EW
                    env_info["tile_size"] = gui_env.tile_size
                if isinstance(inp, guiState):
                    gui_state = inp
                    env_info["state"] = gui_state.state
                if isinstance(inp, guiSteps):
                    gui_steps = inp
                    env_info["step"] = gui_steps.step
                    
    
            log_list.append({"agent_list" : agent_list,
                             "env_info" : env_info,
                             "step" : gui_steps.step})
    else:
        return None

    if log:
        return log_list

    if env_info:
        return env_info

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

    webserver = subprocess.Popen(["python","webserver/server.py"])
    return webserver

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
        "indigo": "midnight"
    }
    color = colors[color]
    return color
    

