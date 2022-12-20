import math
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
from ..objmesh import get_mesh, MatInfo, ObjMesh
import numpy as np
import random
from gym_duckietown import objects
from gym_duckietown.dl_utils import Action
import os
#--------------------------
# Agent Information
#--------------------------

# Agent information, takes environment as a parameter
def get_info(self, env) -> dict:
    info = {}
    pos = self.cur_pos
    angle = self.cur_angle
    
    # Info we care about
    info["agent_id"] = self.agent_id 
    info["color"] = self.color 
    info["last_action"] = self.last_action
    info["robot_speed"] = self.speed
    info["direction"] = self.direction
    info["prev_pos"] = [float(self.prev_pos[0]), float(self.prev_pos[1]), float(self.prev_pos[2])]
    info["cur_pos"] = [float(pos[0]), float(pos[1]), float(pos[2])]
    info["cur_angle"] = float(angle)
    info["tile_coords"] = list(env.get_grid_coords(pos))
    info["lights"] = self.lights 
    info["forward_step"] = self.forward_step
    info["turn_choice"] = self.turn_choice
    info["signal_choice"] = self.signal_choice
    info["curve"] = self.curve   
    info["state"] = self.state 
    info["learning_state"] = self.learning_state 
    info["step_count"] = self.step_count 
    
    # return the dict
    return info

# Get current direction
def get_direction(self, env):
    # Get state information
    curr_angle = self.get_curr_angle(env)

    # Based on the current angle of the agent return a direction it is moving
    if curr_angle > 45 and curr_angle <= 135:
        return 'N'
    elif curr_angle > 135   and curr_angle <= 225:
        return 'W'
    elif curr_angle > 225  and curr_angle <= 315:
        return 'S'
    else:
        return 'E'

def get_curve(self, env):
    """ South:
    Left [0]
    Straight [1]
    Right [2]

    East:
    Left [3]
    Straight [4]
    Right [5]

    North:
    Left [6]
    Straight [7]
    Right [8]

    South:
    Left [9]
    Straight [10]
    Right [11]
    """
    if self.get_direction(env) == 'S':
        if self.turn_choice == 'Left':
            return 0
        if self.turn_choice == 'Straight':
            return 1
        if self.turn_choice == 'Right':
            return 2
    elif self.get_direction(env) == 'E':
        if self.turn_choice == 'Left':
            return 3
        if self.turn_choice == 'Straight':
            return 4
        if self.turn_choice == 'Right':
            return 5
    elif self.get_direction(env) == 'N':
        if self.turn_choice == 'Left':
            return 6
        if self.turn_choice == 'Straight':
            return 7
        if self.turn_choice == 'Right':
            return 8
    elif self.get_direction(env) == 'W':
        if self.turn_choice == 'Left':
            return 9
        if self.turn_choice == 'Straight':
            return 10
        if self.turn_choice == 'Right':
            return 11

# Get current angle degrees
def get_curr_angle(self, env):
    curr_angle = round(math.degrees(self.cur_angle))
    if curr_angle < 0:
        curr_angle = 360 - abs(curr_angle)
    return curr_angle

# Get current tile info
def get_curr_tile(self, env):
    tile_x, tile_z = list(env.get_grid_coords(self.cur_pos))
    tile = env._get_tile(tile_x, tile_z)
    return tile

    # Check if agent is in bounds
def in_bounds(self, env):
    if self.cur_pos[0] < 0 or \
        self.cur_pos[2] < 0 or \
        self.cur_pos[0] > env.grid_width * env.road_tile_size or \
        self.cur_pos[2] > env.grid_height * env.road_tile_size:
        return False
    else:
        return True

# check if already going to complete intersection action
def completing_intersection(self):
    for action in self.actions:
        if action[1] == Action.INTERSECTION_FORWARD:
            return True
    else:
        return False

# Get duckiebot mesh
def get_duckiebot_mesh(color: str) -> ObjMesh:
    change_materials: Dict[str, MatInfo]

    color = np.array(get_duckiebot_color_from_colorname(color))[:3]
    change_materials = {
        "gkmodel0_chassis_geom0_mat_001-material": {"Kd": color},
        "gkmodel0_chassis_geom0_mat_001-material.001": {"Kd": color},
    }

    return get_mesh("duckiebot", change_materials=change_materials)

# Check if a tile is an intersection tile
def intersection_tile(env, tile_x, tile_z):
    if tile_x >= 0 and tile_z >= 0 and tile_x < env.grid_width and tile_z < env.grid_height:
        tile_kind = get_tile(env, tile_x, tile_z)['kind']
        if tile_kind == '4way':
            return True
        else:
            return False
    else:
        return False

# Get tile info
def get_tile(env, tile_x, tile_z):
    return env._get_tile(tile_x, tile_z)

# Get color
def get_duckiebot_color_from_colorname(color: str) -> List[float]:
    colors = {
        "green": [0, 0.5, 0, 1],
        "red": [0.6, 0, 0, 1],
        "grey": [0.3, 0.3, 0.3, 1],
        "blue": [0.0, 0.1, 0.6, 1],
        "cyan": [0, 0.9, 0.9, 1],
        "yellow": [0.8, 0.8, 0.0, 1],
        "orange": [0.9, 0.5, 0.0, 1],
        "midnight": [0.3, 0.0, 0.3, 1],
    }
    color = colors[color]
    return color