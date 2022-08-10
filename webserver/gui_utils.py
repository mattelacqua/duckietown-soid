from gym_duckietown import agents, simulator, objects, logger
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
import numpy as np
import math
import pickle
import io
import subprocess
import os
import signal

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
        return self.state 

# Class for any agent changes
class guiAgent():
    change: str     # Should be 'angle' 'pos' 'inc_pos' 'inc_speed'
    agent_id: str 
    color: str
    cur_pos: List[float]
    cur_angle: float
    inc_direction: str
    lights:  List
    state: str
    
    
    def __init__(self,
        change = "",
        agent_id = "",
        cur_pos = {},
        cur_angle = -1.0,
        color = "",
        inc_direction = "",
        lights = [],
        state = ""):

        self.change = change
        self.agent_id = agent_id
        self.color = color
        self.cur_pos = cur_pos
        self.cur_angle = cur_angle
        self.inc_direction = inc_direction
        self.lights = lights
        self.state = state


    # Handle agent input. Based on the kind of change, do xyz
    def handle_input(self, env):
        agent_id = self.agent_id
        cur_pos = self.cur_pos
        cur_angle = math.radians(self.cur_angle)
        change = self.change
        lights = self.lights
        color = self.color
        state = self.state

        for agent in env.agents:
            if agent.agent_id == agent_id:
                #print("Changing {0}'s current angle from {1} to {2}".format(agent.agent_id, agent.cur_angle, cur_angle))
                if change == "angle":
                    agent.cur_angle = cur_angle
                elif change == "pos":
                    agent.cur_pos = cur_pos
                elif change == "inc_pos":
                    if self.inc_direction == 'N':
                        agent.cur_pos[2] -= 0.1
                    elif self.inc_direction == 'S':
                        agent.cur_pos[2] += 0.1
                    elif self.inc_direction == 'E':
                        agent.cur_pos[0] += 0.1
                    elif self.inc_direction == 'W':
                        agent.cur_pos[0] -= 0.1
                elif change == "lights":
                    for light in lights:
                        agent.set_light(light["light"], light["on"])
                
                #Resetting the actions for the agent
                agent.actions = []

        # Return false because not done command
        return state 


# Serialize by pickling to fifo
def serialize(obj, fifo):
    pickled =  pickle.dumps(obj)
    fifo.write(pickled)
    fifo.flush()

# Unserialize from fifo
def unserialize(fifo):
    while True:
        try:
            fifo.flush()
            o = pickle.load(fifo)
        except EOFError:
            break
        else:
            return o

# Init agents in server
def init_server(fifo, env):
    env.map_jpg(background=True)
    env.map_jpg(background=False)
    agents = env.agents
    input_list = []

    # Initialize the server with agent information
    if agents:
        for agent in agents:
            agent_lights = agent.lights_to_dictlist()
            cur_pos_dict = {'x':round(agent.cur_pos[0], 3),
                            'y':round(agent.cur_pos[2], 3)}
            gui_agent = guiAgent(agent_id=agent.agent_id, 
                                 cur_pos=cur_pos_dict,
                                 cur_angle=round(math.degrees(agent.cur_angle)),
                                 color=html_color(agent.color),
                                 lights=agent_lights)
            input_list.append(gui_agent)

    # Include information about the environment
    gui_env = guiEnv(max_NS=env.grid_height*env.road_tile_size,
                     max_EW=env.grid_width*env.road_tile_size,
                     tile_size=env.road_tile_size)

    input_list.append(gui_env)

    # Serialize the input
    serialize(input_list, fifo)
    
# Read initial positions and env info
def read_init(fifo):
    agent_list =[] 
    env_info = {}
    
    inputs = unserialize(fifo)

    # for each input from init server
    id_no = 0
    if inputs:
        for inp in inputs:
            # if agent add relevant info for webserver to have
            if isinstance(inp, guiAgent):
                gui_agent = inp
                agent_list.append({
                                    "id" : id_no,
                                    "agent_id" : gui_agent.agent_id,
                                    "cur_pos" : gui_agent.cur_pos,
                                    "cur_angle" : gui_agent.cur_angle,
                                    "color" : gui_agent.color,
                                    "lights" : gui_agent.lights
                                    })
                id_no += 1

            # if env_info add relevant info for webserver to have
            if isinstance(inp, guiEnv):
                gui_env = inp
                env_info["max_NS"] = gui_env.max_NS
                env_info["max_EW"] = gui_env.max_EW
                env_info["tile_size"] = gui_env.tile_size
    else:
        return None, None

    if agent_list and env_info:
        return agent_list, env_info
    elif agent_list:
        return agent_list, None
    elif env_info:
        return None, env_info

# Kill old webserver if it exists, otherwise start new subprocess.
def start_webserver():
    cmd = ['pgrep -f .*python3.*webserver/server.py']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    my_pid, err = process.communicate()

    if len(my_pid.splitlines()) >0:
       print("Old webserver running. Killing old and starting up new")
       os.kill(int(my_pid.decode("utf-8")), signal.SIGTERM)
    else:
      print("Old webserver not Running, Starting up new")

    webserver = subprocess.Popen(["python3","webserver/server.py"])

# Get html color
def html_color(color: str):
    colors = {
        "green": "Green",
        "red": "FireBrick",
        "grey": "DimGray",
        "blue": "DarkBlue",
        "cyan": "Cyan",
        "yellow": "Gold",
        "orange": "Orange",
        "midnight": "Indigo"
    }
    color = colors[color]
    return color
    

