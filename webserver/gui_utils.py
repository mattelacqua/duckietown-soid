from gym_duckietown import agents, simulator, objects, logger
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
import numpy as np
import math
import pickle
import subprocess
import os
import signal
import time

# Send information through guiEnv
class guiEnv():
    max_NS: int
    max_EW: int
    tile_size: int
    map_image: None

    def __init__(self,
        max_NS = 0,
        max_EW = 0,
        tile_size = 0):

        self.max_NS = max_NS
        self.max_EW = max_EW
        self.tile_size = tile_size

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
    log_lights: List
    log_pos: List
    log_angle: None
    log_color: None
    
    
    def __init__(self,
        change = "",
        agent_id = "",
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
        signal_choice= None,
        log_lights= None,
        log_pos= None,
        log_angle= None,
        log_color= None,
        ):

        self.change = change
        self.agent_id = agent_id
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
    pickled = pickle.dumps(obj)
    fifo.write(pickled)
    fifo.flush()
    toc = time.perf_counter()
    #print("Serialize Time = {0}".format(toc - tic))

# Unserialize from fifo
def unserialize(fifo, log=False):
    tic = time.perf_counter()
    while True:
        try:
            yield pickle.load(fifo)
        except EOFError:
            break
            toc = time.perf_counter()
            #print("EOF Unserialize = {0}".format(toc - tic))
        #else:
            #return o
            #toc = time.perf_counter()
            #print("Success Unserialize = {0}".format(toc - tic))
    


# Init agents in server
def init_server(dt, fifo, env, socket, get_map=False):


    print(f"Env Step {env.step}")
    tic = time.perf_counter()
    if get_map:
        env.map_jpg(background=True)
        env.map_jpg(background=False)
    agents = env.agents
    input_list = []
    step = env.agents[0].step_count

    # Initialize the server with agent information
    if agents:
       input_list.extend(list(map(lambda agent: guiAgent(agent_id=agent.agent_id,
                                                         cur_pos={'x':round(agent.cur_pos[0], 3),
                                                                  'y':round(agent.cur_pos[2], 3)},
                                                         cur_angle=round(math.degrees(agent.cur_angle)),
                                                         color=html_color(agent.color),
                                                         turn_choice=agent.turn_choice,
                                                         signal_choice=agent.signal_choice,
                                                         forward_step=agent.forward_step,
                                                         bbox_offset_w=agent.bbox_offset_w,
                                                         bbox_offset_l=agent.bbox_offset_l,
                                                         state=agent.state,
                                                         lights=agent.lights_to_dictlist(),
                                                         log_lights=agent.lights,
                                                         log_color=agent.color,
                                                         log_pos=agent.cur_pos,
                                                         log_angle=agent.cur_angle



                                                         ), agents)))

    # Include information about the environment
    gui_env = guiEnv(max_NS=env.grid_height*env.road_tile_size,
                     max_EW=env.grid_width*env.road_tile_size,
                     tile_size=env.road_tile_size)

    input_list.append(gui_env)

    #print(f"Sending The webserver {env.state}")
    gui_state = guiState(state=env.state)
    input_list.append(gui_state)

    gui_step = guiSteps(step=step)
    input_list.append(gui_step)

    toc = time.perf_counter()
    #print("Data Function Dict Traversal = {0}".format(toc - tic))
    # Serialize the input
    serialize(input_list, fifo)


    if socket:
        socket.emit("update_sim_info")
  
    
    
# Read initial positions and env info
def read_init(fifo, log=False):
    agent_list =[] 
    env_info = {}
    log_list = []
    
    input_list = list(unserialize(fifo, log))
    if log:
        print(f"Input list is {input_list}")
        fifo.seek(0)


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
        return None, None

    if log:
        return log_list

    if agent_list and env_info:
        return agent_list, env_info
    elif agent_list:
        return agent_list, None
    elif env_info:
        return None, env_info
    else:
        return None, None

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
    

