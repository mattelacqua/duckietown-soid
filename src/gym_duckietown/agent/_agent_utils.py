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
    # Get the position relative to the right lane tangent

    info["agent_id"] = self.agent_id 
    info["action"] = self.last_action
    info["robot_speed"] = self.speed
    info["prev_pos"] = [float(self.prev_pos[0]), float(self.prev_pos[1]), float(self.prev_pos[2])]
    info["cur_pos"] = [float(pos[0]), float(pos[1]), float(pos[2])]
    info["cur_angle"] = float(angle)
    info["wheel_velocities"] = [self.wheelVels[0], self.wheelVels[1]]
    info["tile_coords"] = list(env.get_grid_coords(pos))
    info["lights"] = self.lights 
    info["actions"] = self.actions 
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


# Get current angle degrees
def get_curr_angle(self, env):
    info = self.get_info(env)
    curr_angle = round(math.degrees(info['cur_angle']))
    if curr_angle < 0:
        curr_angle = 360 - abs(curr_angle)
    return curr_angle

# Get current tile info
def get_curr_tile(self, env):
    info = self.get_info(env)
    tile_x, tile_z = info['tile_coords']
    tile = env._get_tile(tile_x, tile_z)
    """if tile == None:
        print(f"Failed at tile {tile_x} {tile_z}")
        print(f"Failed at pos {self.cur_pos}")"""
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

def completing_intersection(self):
    # check if already going to complete intersection action
    for action in self.actions:
        #print(action[1])
        if action[1] == Action.INTERSECTION_FORWARD or action[1] == Action.INTERSECTION_LEFT or action[1] == Action.INTERSECTION_RIGHT:
            print("THIS IS THE CASE WE ARE HITTING")
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