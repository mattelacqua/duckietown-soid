from .dl_utils import *
from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
from .objmesh import get_mesh, MatInfo, ObjMesh
import numpy as np
import random
from . import logger
from gym_duckietown import objects
import os
from .agent._agent_utils import get_duckiebot_mesh

"""
Contains functions for moving agent in ite world scenarios.
"""
so_file = str(os.getcwd()) + "/src/gym_duckietown/decision_logic/libdecision_logic.so"
dl = CDLL(so_file)

class Agent():
    cur_pos: np.ndarray
    cur_angle: np.ndarray
    last_action: Action
    actions: Union[List[np.ndarray], Action]
    wheelsVels: np.ndarray
    step_count: int
    intersection_arrival: int
    start_tile: List[int] 
    start_pose: List[Union[List[Union[float, int]], Union[float, int]]] 
    speed: float 
    color: str 
    timestamp: float 
    agent_id: str 
    nearby_objects: List[objects.WorldObj]         # Keep track of nearby objects and agents
    nearby_agents: List
    intersection_agents: List
    follow_dist: float
    max_iterations: int
    turn: str
    signal_choice: str
    stop_point: float
    forward_step: float
    bbox_offset_w: float
    bbox_offset_l: float
    random_spawn: bool
    reward_profile: int
    learning_state: List[bool]
    states: dict
    direction: str
    start_angle: float

    def __init__(self,
        cur_pos=[0.0, 0.0, 0.0],
        cur_angle=0.0,
        start_tile=(0, 0),
        start_pose=[[0.0, 0.0, 0.0], 0.0],
        agent_id="ID",
        random_spawn=False,
        color="red"):
        
        self.cur_pos = cur_pos
        self.prev_pos = cur_pos
        self.cur_angle = cur_angle
        self.start_tile = start_pose
        self.speed = 0.0
        self.agent_id = agent_id 
        self.last_action = None 
        self.wheelVels = np.array([0, 0])
        self.timestamp = 0.0
        self.start_tile = start_tile
        self.start_pose = start_pose
        self.state = None
        self.color = color
        self.mesh = get_duckiebot_mesh(color)
        self.nearby_objects = []          # Keep track of nearby objects and agents
        self.nearby_agents = []
        self.intersection_agents = []
        self.actions = []
        self.step_count = 0
        self.follow_dist = 0.3
        self.random_spawn = random_spawn
        self.max_iterations = 1000
        height = 0.05
        self.lights =   {
                        "front_left": [0.1, -0.05, height, True],
                        "front_right": [0.1, +0.05, height, False],
                        "center": [0.1, +0.0, height, False],
                        "back_left": [-0.1, -0.05, height, False],
                        "back_right": [-0.1, +0.05, height, False],
                        }
        self.turn_choice = None
        self.signal_choice = None
        self.stop_point = None
        self.forward_step = 0.00
        self.bbox_offset_w = 0.00
        self.bbox_offset_l = 0.00
        self.intersection_arrival = None
        self.reward_profile = None
        self.learning_state = [0,0,0,0,0,0,0,0,0,0]
        self.states = {}
        self.direction ='' 
        self.curve = 0

    # Import things for learning
    from .agent._agent_learning import  get_learning_state, \
                                        get_reward, \
                                        get_state

    # Import things for decision logic
    from .agent._agent_decision_logic import  proceed, \
                                        handle_proceed, \
                                        has_right_of_way, \
                                        in_intersection, \
                                        at_intersection_entry,\
                                        intersection_empty, \
                                        object_in_range, \
                                        is_tailgating, \
                                        is_behind, \
                                        cars_waiting_to_enter, \
                                        cars_arrived_before_me, \
                                        car_entering_range

    # Import Lights
    from .agent._agent_lights import    turn_on_light, \
                                        turn_off_light, \
                                        set_light, \
                                        lights_to_dictlist, \
                                        signal_for_turn

    # Import Movement Functions
    from .agent._agent_movement import  stop_vehicle, \
                                        move_forward, \
                                        straighten_out, \
                                        get_turn_overcomp

    # Import Intersection Detection/Handling Functions
    from .agent._agent_intersection import  handle_intersection, \
                                            intersection_detected, \
                                            approaching_intersection, \
                                            left_intersection, \
                                            get_stop_pos
        
    # Import Object Detection/Handling Functions
    from .agent._agent_objects import   get_nearby_obstacles, \
                                        get_obstacles, \
                                        reset_obstacles, \
                                        handle_agents, \
                                        handle_objects

    # Import rendering functions
    from .agent._agent_rendering import render_step, \
                                        render_step_inner, \
                                        completing_action, \
                                        get_next_action, \
                                        add_actions

    # Import utilities
    from .agent._agent_utils import get_info, \
                                    get_direction, \
                                    get_curr_angle, \
                                    get_curve, \
                                    get_curr_tile, \
                                    in_bounds

