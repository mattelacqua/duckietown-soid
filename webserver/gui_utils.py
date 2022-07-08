from gym_duckietown import agents, simulator, objects, logger
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
import numpy as np
import math
import pickle
import io

class guiInput():
    agent: bool
    agent_id: str 
    obj: bool
    obj_id: str
    tile: bool
    cur_pos: List[float]
    cur_angle: float
    tile_pos: List[int]

    def __init__(self,
        agent = False,
        agent_id = "",
        obj = False,
        obj_id = "",
        tile = False,
        cur_pos = [],
        cur_angle = 0.0,
        color = "",
        tile_pos = []):

        self.agent = agent
        self.agent_id = agent_id
        self.obj = obj
        self.obj_id = obj_id
        self.tile = tile
        self.cur_pos = cur_pos
        self.cur_angle = cur_angle
        self.tile_pos = tile_pos
        self.color = color



    def handle_input(self, env):
        if self.agent:
            agent_id = self.agent_id
            cur_pos = self.cur_pos
            cur_angle = math.radians(self.cur_angle)

            for agent in env.agents:
                if agent.agent_id == agent_id:
                    #print("Changing {0}'s current angle from {1} to {2}".format(agent.agent_id, agent.cur_angle, cur_angle))
                    agent.cur_angle = cur_angle


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
def init_server(fifo, agents=[], objs=[]):
    agent_list = []
    obj_list = []

    if agents:
        for agent in agents:
            gui_agent = guiInput(agent=True, 
                                 agent_id=agent.agent_id, 
                                 cur_pos=agent.cur_pos,
                                 cur_angle=agent.cur_angle,
                                 color=html_color(agent.color))
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
    return agent_list


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
    

