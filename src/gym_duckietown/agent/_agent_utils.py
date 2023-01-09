import math
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
from ..objmesh import get_mesh, MatInfo, ObjMesh
import numpy as np
from gym_duckietown import objects
from gym_duckietown.dl_utils import Action
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



def get_curve(self, env, straight=False, follow_pos=None):
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
    if not self.get_curr_tile(env):
        return None

    tile = self.get_curr_tile(env)
    direction = self.get_direction(env)
    follow_tile = None

    if follow_pos:
        tile_x, tile_z = list(env.get_grid_coords(follow_pos))
        follow_tile = env._get_tile(tile_x, tile_z)
        if not follow_tile:
            return None
        if tile['kind'] == '4way' and follow_tile['kind'] != ['4way']:
            if self.start_direction == 'N' and self.turn_choice == 'Left':
                direction = 'W'
            elif self.start_direction == 'N' and self.turn_choice == 'Right':
                direction = 'E'
            elif self.start_direction == 'S' and self.turn_choice == 'Left':
                direction = 'E'
            elif self.start_direction == 'S' and self.turn_choice == 'Right':
                direction = 'W'
            elif self.start_direction == 'E' and self.turn_choice == 'Left':
                direction = 'N'
            elif self.start_direction == 'E' and self.turn_choice == 'Right':
                direction = 'S'
            elif self.start_direction == 'W' and self.turn_choice == 'Left':
                direction = 'S'
            elif self.start_direction == 'W' and self.turn_choice == 'Right':
                direction = 'N'
            straight=True
        if tile['kind'] != '4way' and follow_tile['kind'] == ['4way']:
            direction = self.start_direction
            straight=False
        if tile['kind'] == '4way' and follow_tile['kind'] == ['4way']:
            direction = self.start_direction
            straight=False
        if tile['kind'] != '4way' and follow_tile['kind'] != ['4way']:
            straight=True
        tile = follow_tile

    else:
        if tile['kind'] != '4way':
            straight=True
        elif tile['kind'] == '4way':
            straight=False
            direction=self.start_direction

        
    if straight:
        if direction == 'N':
            if tile['angle'] == 0:
                return 1
            elif tile['angle'] == 2:
                return 0
        elif direction == 'S':
            if tile['angle'] == 0:
                return 0
            elif tile['angle'] == 2:
                return 1
        elif direction == 'W':
            if tile['angle'] == 1:
                return 1
            elif tile['angle'] == 3:
                return 0
        elif direction == 'E':
            if tile['angle'] == 1:
                return 0
            elif tile['angle'] == 3:
                return 1
        
        return None
    if direction == 'S':
        if self.turn_choice == 'Left':
            return 0
        if self.turn_choice == 'Straight':
            return 1
        if self.turn_choice == 'Right':
            return 2
    elif direction == 'E':
        if self.turn_choice == 'Left':
            return 3
        if self.turn_choice == 'Straight':
            return 4
        if self.turn_choice == 'Right':
            return 5
    elif direction == 'N':
        if self.turn_choice == 'Left':
            return 6
        if self.turn_choice == 'Straight':
            return 7
        if self.turn_choice == 'Right':
            return 8
    elif direction == 'W':
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



# Get duckiebot mesh
def get_duckiebot_mesh(color: str) -> ObjMesh:
    change_materials: Dict[str, MatInfo]

    color = np.array(get_duckiebot_color_from_colorname(color))[:3]
    change_materials = {
        "gkmodel0_chassis_geom0_mat_001-material": {"Kd": color},
        "gkmodel0_chassis_geom0_mat_001-material.001": {"Kd": color},
    }

    return get_mesh("duckiebot", change_materials=change_materials)



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