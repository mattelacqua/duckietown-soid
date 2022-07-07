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
        tile_pos = []):

        self.agent = agent
        self.agent_id = agent_id
        self.obj = obj
        self.obj_id = obj_id
        self.tile = tile
        self.cur_pos = cur_pos
        self.cur_angle = cur_angle
        self.tile_pos = tile_pos


    def serialize(self):
        return pickle.dumps(self)

    def handle_input(self, env):
        if self.agent:
            agent_id = self.agent_id
            cur_pos = self.cur_pos
            cur_angle = math.radians(self.cur_angle)

            for agent in env.agents:
                if agent.agent_id == agent_id:
                    #print("Changing {0}'s current angle from {1} to {2}".format(agent.agent_id, agent.cur_angle, cur_angle))
                    agent.cur_angle = cur_angle



def unserialize(fifo):
    while True:
        try:
            o = pickle.load(fifo)
        except EOFError:
            break
        else:
            return o

    
    

