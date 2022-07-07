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

def unserialize(fifo):
    while True:
        print("HERE")
        try:
            o = pickle.load(fifo)
        except EOFERROR:
            break
        else:
            return o
    

