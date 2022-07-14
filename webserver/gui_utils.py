from gym_duckietown import agents, simulator, objects, logger
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
import numpy as np
import math
import pickle
import io

class guiInput():
    agent: bool
    agent_id: str 
    pos: str 
    obj: bool
    obj_id: str
    tile: bool
    cur_pos: List[float]
    cur_angle: float
    tile_pos: List[int]
    done: bool
    max_NS: int
    max_EW: int
    inc_direction: str

    def __init__(self,
        agent = False,
        agent_id = "",
        change = "",
        obj = False,
        obj_id = "",
        tile = False,
        cur_pos = [],
        cur_angle = -1.0,
        color = "",
        tile_pos = [],
        done = False,
        max_NS = 0,
        max_EW = 0,
        inc_direction = ""):

        self.agent = agent
        self.agent_id = agent_id
        self.obj = obj
        self.obj_id = obj_id
        self.tile = tile
        self.cur_pos = cur_pos
        self.cur_angle = cur_angle
        self.tile_pos = tile_pos
        self.color = color
        self.done = done
        self.max_NS = max_NS
        self.max_EW = max_EW
        self.change = change
        self.inc_direction = inc_direction



    def handle_input(self, env):
        if self.done:
            return True
        if self.agent:
            agent_id = self.agent_id
            cur_pos = self.cur_pos
            cur_angle = math.radians(self.cur_angle)
            change = self.change

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
                    
                    #Resetting the actions for the agent
                    agent.actions = []
            return False


def serialize(obj, fifo):
    pickled =  pickle.dumps(obj)
    fifo.write(pickled)
    fifo.flush()

def unserialize(fifo):
    while True:
        try:
            o = pickle.load(fifo)
        except EOFError:
            break
        else:
            return o

# Init agents in server
def init_server(fifo, env):
    agents = env.agents
    objects = env.objects
    

    agent_list = []
    obj_list = []

    if agents:
        for agent in agents:
            gui_agent = guiInput(agent=True, 
                                 agent_id=agent.agent_id, 
                                 cur_pos=agent.cur_pos,
                                 cur_angle=round(math.degrees(agent.cur_angle)),
                                 color=html_color(agent.color),
                                 max_NS=env.grid_height*env.road_tile_size,
                                 max_EW=env.grid_width*env.road_tile_size)
            agent_list.append(gui_agent)
    serialize(agent_list, fifo)

# Read initial positions
def read_init(fifo):
    agent_list = []
    agents = unserialize(fifo)
    for agent in agents:
        agent_list.append({
                            "agent_id" : agent.agent_id,
                            "cur_pos" : agent.cur_pos,
                            "cur_angle" : agent.cur_angle,
                            "color" : agent.color
                          })
    env_info = {}
    env_info["max_NS"] = agents[0].max_NS
    env_info["max_EW"] = agents[0].max_EW
    return agent_list, env_info 


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
    

