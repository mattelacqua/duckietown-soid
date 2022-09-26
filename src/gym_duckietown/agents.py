from .dl_utils import *

from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
from .objmesh import get_mesh, MatInfo, ObjMesh
import numpy as np
import random
import numpy as np
import math
from . import logger
from gym_duckietown import objects
import os

so_file = str(os.getcwd()) + "/src/gym_duckietown/decision_logic/libdecision_logic.so"
dl = CDLL(so_file)

"""
Contains functions for moving agent in ite world scenarios.
"""

class Agent():
    cur_pos: np.ndarray
    cur_angle: np.ndarray
    last_action: np.ndarray
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
        self.last_action = np.array([0, 0])
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

#--------------------------
# Decision Logic
#--------------------------
    def proceed(self, env, good_agent=False):

        # If we are good we want to avoid tailgating
        if good_agent and self.is_tailgating(env):
            no_intersection_stop_actions = []
            for action in self.actions:
                if action[1] != Action.INTERSECTION_STOP:
                    no_intersection_stop_actions.append(action)
            action = np.array([0.0, 0.0])
            self.actions = [(action, Action.STOP)] + no_intersection_stop_actions

            return
        elif good_agent and not self.is_tailgating(env):
            no_stop_actions = []
            for action in self.actions:
                if action[1] != Action.STOP:
                    no_stop_actions.append(action)
                #else:
                    #print("Removing a stop action")
            self.actions = no_stop_actions

            return

        # Check how many actions are stop
        """stop_count = 0
        for action in self.actions:
            if action[1] = Action.STOP or action[1] == Action.INTERSECTION_STOP:
                stop_count += 1"""

        # Gather all the information we need:
        # Range we care about
        #radius = ((env.road_tile_size / 3) * 2)
        radius = (env.road_tile_size)

        #print(f"Radius {radius}")
        in_intersection = self.in_intersection(env)
        at_entry = self.at_intersection_entry(env)
        intersection_empty = self.intersection_empty(env)
        intersection_in_range = self.approaching_intersection(env)
        object_in_range, obj = self.object_in_range(env, location="Ahead", radius=radius)

        # Get car directly in front of us things:
        ahead_car_intersection_in_range = obj.approaching_intersection(env) if obj else False
        ahead_car_object_in_range, obj = obj.object_in_range(env, location="Ahead", radius=radius) if obj else False, None

        # See if a car is entering our range
        car_entering_our_range = self.car_entering_range(env, radius=radius)

        # Check behind us
        car_behind_us_in_intersection = self.object_in_range(env, location="Behind", intersection=True, radius=radius)
        car_behind_us_out_intersection = self.object_in_range(env, location="Behind", intersection=False, radius=radius)

        """print(f"{self.agent_id} State")
        print(f"In Intersection: {in_intersection}")
        print(f"At Entry: {at_entry}")
        print(f"Intersection Empty: {intersection_empty}")
        print(f"Intersection In Range: {intersection_in_range}")
        print(f"Object In Range: {object_in_range}")
        print(f"Car Ahead of us Intersection In Range: {ahead_car_intersection_in_range}")
        print(f"Car Ahead of us Object In Range: {ahead_car_object_in_range}")
        print(f"Car Entering Range: {car_entering_our_range}")
        print(f"Car Behind us (Us in intersection): {car_behind_us_in_intersection}")
        print(f"Car Behind us (Us NOT in intersection): {car_behind_us_out_intersection}")"""

        dl.proceed.argtypes = [AgentState, c_bool]
        dl.proceed.restype = c_bool

        agent_state_struct = AgentState(in_intersection, 
                                        at_entry, 
                                        intersection_empty, 
                                        intersection_in_range, 
                                        object_in_range, 
                                        ahead_car_intersection_in_range,
                                        ahead_car_object_in_range,
                                        car_entering_our_range,
                                        car_behind_us_in_intersection,
                                        car_behind_us_out_intersection)
        should_proceed = dl.proceed(agent_state_struct, good_agent)
        self.handle_proceed(should_proceed)

    # Handle wheather or not we should proceed.
    def handle_proceed(self, should_proceed):
        if not should_proceed:
            no_intersection_stop_actions = []
            for action in self.actions:
                if action[1] != Action.INTERSECTION_STOP:
                    no_intersection_stop_actions.append(action)
            action = np.array([0.0, 0.0])
            self.actions = [(action, Action.STOP)] + no_intersection_stop_actions
        elif should_proceed:
            no_stop_actions = []
            for action in self.actions:
                if action[1] != Action.STOP:
                    no_stop_actions.append(action)
            self.actions = no_stop_actions

    # Check if we are at an intersection
    def in_intersection(self, env):
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        return intersection_tile(env, tile_x, tile_z)

    # Check if we are at an intersection
    def at_intersection_entry(self, env):
        # Get state information
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        direction = self.get_direction(env)

        # Based on direction, check if the next tile is an intersection or if we are at one. 
        close_to_intersection = False
        intersection_coords = None
        if direction == 'N' and (intersection_tile(env, tile_x, tile_z-1) or intersection_tile(env, tile_x, tile_z)):
            if intersection_tile(env, tile_x, tile_z):
                intersection_coords = tile_x, tile_z
            else:
                intersection_coords = tile_x, tile_z-1
            close_to_intersection = True
        elif direction == 'W' and (intersection_tile(env, tile_x-1, tile_z) or intersection_tile(env, tile_x, tile_z)):
            if intersection_tile(env, tile_x, tile_z):
                intersection_coords = tile_x, tile_z
            else:
                intersection_coords = tile_x-1, tile_z
                close_to_intersection = True
        elif direction == 'S' and (intersection_tile(env, tile_x, tile_z+1) or intersection_tile(env, tile_x, tile_z)):
            if intersection_tile(env, tile_x, tile_z):
                intersection_coords = tile_x, tile_z
            else:
                intersection_coords = tile_x, tile_z+1
            close_to_intersection = True
        elif direction == 'E' and (intersection_tile(env, tile_x+1, tile_z) or intersection_tile(env, tile_x, tile_z)):
            if intersection_tile(env, tile_x, tile_z):
                intersection_coords = tile_x, tile_z
            else:
                intersection_coords = tile_x+1, tile_z
            close_to_intersection = True

        if not close_to_intersection:
            return False
        else:
            # Check if we are within a cars length of the stop line.
            if direction == 'N':
                stop_line = (intersection_coords[1] + 1) * env.road_tile_size
                if self.cur_pos[2] > stop_line - env.robot_length/2 and self.cur_pos[2] < stop_line + env.robot_length:
                    return True
            elif direction == 'S':
                stop_line = (intersection_coords[1] + 0 if intersection_coords[1] != 0 else 1) * env.road_tile_size
                if self.cur_pos[2] > stop_line - env.robot_length/2 and self.cur_pos[2] < stop_line + env.robot_length:
                    return True
            elif direction == 'E':
                stop_line = (intersection_coords[0] + 0 if intersection_coords[0] != 0 else 1) * env.road_tile_size
                if self.cur_pos[2] > stop_line - env.robot_length/2 and self.cur_pos[2] < stop_line + env.robot_length:
                    return True
            elif direction == 'W':
                stop_line = (intersection_coords[0] + 1) * env.road_tile_size
                if self.cur_pos[2] > stop_line - env.robot_length/2 and self.cur_pos[2] < stop_line + env.robot_length:
                    return True
            else:
                return False

    # Check if anyone other than us is currently in the intersection
    def intersection_empty(self, env):
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        intersection_empty = True
        for agent in env.agents:
            agent_tile_x, agent_tile_z = agent.get_curr_tile(env)['coords']
            if agent_tile_x == tile_x and agent_tile_z == tile_z and intersection_tile(env, tile_x, tile_z) and agent != self:
                intersection_empty = False
        return intersection_empty


    # See if there is an object within one tile block of a car infront of us
    def object_in_range(self, env, location="Ahead", intersection=None, radius=1, return_multiple=False):
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        direction = self.get_direction(env)
        side_radius = radius
        front_radius = radius / 3

        if direction == 'N':
            # Lower bound for xrange is our current x minus half a tile
            # Upper bound for xrange is our current x plus half a tile
            # Lower bound for zrange is our current z - tilesize
            # Upper bound for zrange is our current z
            object_ahead_range_x_lb = self.cur_pos[0] - side_radius
            object_ahead_range_x_ub = self.cur_pos[0] + side_radius 
            if location == "Ahead":
                object_ahead_range_z_lb = self.cur_pos[2] - front_radius
                object_ahead_range_z_ub = self.cur_pos[2] 
            elif location == "Behind":
                object_ahead_range_z_lb = self.cur_pos[2] + env.robot_length
                object_ahead_range_z_ub = self.cur_pos[2] + front_radius + env.robot_length
        elif direction == 'S':
            # Lower bound for xrange is our current x minus half a tile
            # Upper bound for xrange is our current x plus half a tile
            # Lower bound for zrange is our current z
            # Upper bound for zrange is our current z + tilesize
            object_ahead_range_x_lb = self.cur_pos[0] - side_radius
            object_ahead_range_x_ub = self.cur_pos[0] + side_radius
            if location == "Ahead":
                object_ahead_range_z_lb = self.cur_pos[2] 
                object_ahead_range_z_ub = self.cur_pos[2] + front_radius             
            elif location == "Behind":
                object_ahead_range_z_lb = self.cur_pos[2] - front_radius - env.robot_length
                object_ahead_range_z_ub = self.cur_pos[2] - env.robot_length
        elif direction == 'W':
            # Lower bound for xrange is our current X - tilesize
            # Upper bound for xrange is our current X
            # Lower bound for zrange is our current z minus half a tile
            # Upper bound for zrange is our current z plus half a tile
            if location == "Ahead":
                object_ahead_range_x_lb = self.cur_pos[0] - front_radius
                object_ahead_range_x_ub = self.cur_pos[0] 
            elif location == "Behind":
                object_ahead_range_x_lb = self.cur_pos[0] + env.robot_length
                object_ahead_range_x_ub = self.cur_pos[0] + front_radius + env.robot_length
            object_ahead_range_z_lb = self.cur_pos[2] - side_radius 
            object_ahead_range_z_ub = self.cur_pos[2] + side_radius
        elif direction == 'E':
            # Lower bound for xrange is our current X
            # Upper bound for xrange is our current X + tilesize
            # Lower bound for zrange is our current z minus half a tile
            # Upper bound for zrange is our current z plus half a tile
            if location == "Ahead":
                object_ahead_range_x_lb = self.cur_pos[0] 
                object_ahead_range_x_ub = self.cur_pos[0] + front_radius           
            elif location == "Behind":
                object_ahead_range_x_lb = self.cur_pos[0] - front_radius - env.robot_length
                object_ahead_range_x_ub = self.cur_pos[0] - env.robot_length           
            object_ahead_range_z_lb = self.cur_pos[2] - side_radius
            object_ahead_range_z_ub = self.cur_pos[2] + side_radius

        # Check if any agent is in the tile space length in front of us
        agents_in_radius = []
        for agent in env.agents:
            agent_x, agent_z = agent.cur_pos[0], agent.cur_pos[2]

            # if the agent is not us, check and see if it is within the range
            if agent.agent_id != self.agent_id:
                if agent_x >= object_ahead_range_x_lb and agent_x <= object_ahead_range_x_ub and \
                   agent_z >= object_ahead_range_z_lb and agent_z <= object_ahead_range_z_ub:
                    """print(f"{self.agent_id} at {self.cur_pos} is seeing {agent.agent_id} at {agent.cur_pos}")
                    print(f"xLB is {object_ahead_range_x_lb}")
                    print(f"xUB is {object_ahead_range_x_ub}")
                    print(f"zLB is {object_ahead_range_z_lb}")
                    print(f"zUB is {object_ahead_range_z_ub}")
                    print(f"Radius is {radius}")"""
                    agents_in_radius.append(agent)

        if agents_in_radius and return_multiple:
            if intersection == True and location == "Behind":
                 if intersection_tile(env, tile_x, tile_z): # If we are checking behind us and we are in an intersection
                    return True, agents_in_radius
                 elif not intersection_tile(env, tile_x, tile_z) :
                    return False, None
            elif intersection == False and location == "Behind":# If we are checking behind us and we are NOT in an intersection
                if not intersection_tile(env, tile_x, tile_z):
                    return True, agents_in_radius
                elif intersection_tile(env, tile_x, tile_z):
                    return False, None
            elif intersection == None: # Regular check ahead or behind
                return True, agents_in_radius
        else:
            closest_distance = math.inf
            closest_agent = None
            for agent in agents_in_radius:
                if agent != self:
                    distance = math.dist([agent.cur_pos[0], agent.cur_pos[2]], [self.cur_pos[0], self.cur_pos[2]])
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_agent = agent

            if closest_agent:
                #print(f"{closest_agent.agent_id} IN FRONT OF {self.agent_id}")
                if intersection == True and location == "Behind": # If we are checking behind us and we are in an intersection
                    if intersection_tile(env, tile_x, tile_z):
                        return True, closest_agent
                    elif not intersection_tile(env, tile_x, tile_z):
                        return False, None
                elif intersection == False and location == "Behind":# If we are checking behind us and we are NOT in an intersection
                    if not intersection_tile(env, tile_x, tile_z):
                        return True, closest_agent
                    elif intersection_tile(env, tile_x, tile_z):
                        return False, None
                elif intersection == None: # Regular check ahead or behind
                    return True, closest_agent
            else:
                return False, None
            #TODO FIX THE CHECK BEHIND AND AHEAD NONSENSE BECAUSE SOMETHING IS FUBAR

    def is_tailgating(self, env):
        for agent in env.agents:
            #print(f"Comparing Agent {self} to {agent}")
            #print(f"Comparing Agent {self.agent_id} {self.color} to {agent.agent_id} {agent.color}")
            if agent.agent_id != self.agent_id:
                info = agent.get_info(env)
                agent_direction = agent.get_direction(env)
                agent_x, agent_z = env.get_grid_coords(info['cur_pos'])
                prev_distance = env.pos_distance(self.get_prev_pos(env, matrix=True), \
                                                 agent.get_prev_pos(env, matrix=True))
                curr_distance = env.pos_distance(self.get_curr_pos(env, matrix=True), \
                                                 agent.get_curr_pos(env, matrix=True))
                if  agent_direction == self.get_direction(env) and \
                    prev_distance > curr_distance and \
                    curr_distance < env.robot_length*3 and \
                    self.is_behind(env, agent):
                                print(f"Agent {self.color} is tailgating {agent.color}")
                                return True
        return False

    def is_behind(self, env, agent):
        #print("CHECKING BEHIND")
        direction = self.get_direction(env)
        if direction == 'N':
            if agent.cur_pos[2] < self.cur_pos[2]:
                return True
        elif direction == 'S':
            if agent.cur_pos[2] > self.cur_pos[2]:
                return True
        elif direction == 'E':
            if agent.cur_pos[0] > self.cur_pos[0]:
                return True
        elif direction == 'W':
            if agent.cur_pos[0] < self.cur_pos[0]:
                return True
        else:
            return False

    



    # See if a car is entering out range
    def car_entering_range(self, env, radius=1):
        cars_are_in_large_range, cars_large_range = self.object_in_range(env, location="Ahead", radius=radius*2, return_multiple=True)
        cars_are_in_short_range, cars_short_range = self.object_in_range(env, location="Ahead", radius=radius, return_multiple=True)

        if cars_are_in_large_range and cars_are_in_short_range:
            cars_approaching = list(set(cars_large_range) - set(cars_short_range))
        elif cars_are_in_large_range and not cars_are_in_short_range:
            cars_approaching = cars_large_range
        else:
            return False

        car_entering_our_range = False
        for agent in cars_approaching:
            curr_distance = math.dist([agent.cur_pos[0], agent.cur_pos[2]], [self.cur_pos[0], self.cur_pos[2]])
            prev_distance = math.dist([agent.prev_pos[0], agent.prev_pos[2]], [self.prev_pos[0], self.prev_pos[2]])
            if curr_distance < prev_distance:
                car_entering_our_range = True

        return car_entering_our_range




#--------------------------
# Lights
#--------------------------

    # Turn on Specific Light
    def turn_on_light(self, light):
        self.lights[light][3] = True

    # Turn off Specific Light
    def turn_off_light(self, light):
        self.lights[light][3] = False

    # Set light
    def set_light(self, light, on):
        if on:
            self.lights[light][3] = True
        else:
            self.lights[light][3] = False

    # Lights to Dict
    def lights_to_dictlist(self):
        light_list = []
        for light in self.lights.items():
            light_list.append({"light": light[0], "on":self.lights[light[0]][3]})
        return light_list

    # Signal for a turn
    def signal_for_turn(self, turn):
        choices = ['Right', 'Left', 'Straight'] 
        if not turn:
            turn = random.choice(choices)

        if turn == "Right":
            self.turn_on_light("front_right")
            self.turn_on_light("back_right")
            self.turn_off_light("front_left")
            self.turn_off_light("back_left")
            self.turn_off_light("center")
        elif turn == "Left":
            self.turn_off_light("front_right")
            self.turn_off_light("back_right")
            self.turn_on_light("front_left")
            self.turn_on_light("back_left")
            self.turn_off_light("center")
        elif turn == "Straight":
            self.turn_off_light("front_right")
            self.turn_off_light("back_right")
            self.turn_off_light("front_left")
            self.turn_off_light("back_left")
            self.turn_off_light("center")

   
#--------------------------
# Movement
#--------------------------

    # Stop the vehicle
    def stop_vehicle(self, env, signal_choice, stop_point: int=30,forward_step: float=0.44):
        if env.verbose:
            logger.info(self.agent_id + ": Stopping")
        stop_iterations = 0

        # Initialize action sequence
        action_seq = []

        # While still moving Slow down
        while stop_iterations < stop_point:
            action = np.array([0.0, 0.0])
            action_seq.append((action, Action.INTERSECTION_STOP))
            self.signal_for_turn(signal_choice)
            stop_iterations += 1

        return action_seq

 
    # Move Forwards at whatever angle we are at, not going faster than 30 mps
    def move_forward(self, env, speed_limit=1.0):
        #print(dl.square(5))
        #print("\n\n\n\n\n\n\n")
        # Set the speed
        forward_step = self.forward_step
        if forward_step == 0.0:
            return []

        # Get state information
        curr_speed = self.get_curr_speed(env)
        if env.verbose:
            logger.info(self.agent_id + ": Moving Forwards at speed " + str(curr_speed))

        # Initialize action sequence
        action_seq = []

        # While still moving Slow down
        if curr_speed > speed_limit:
            action = np.array([0.0, 0.0])
            action_seq.append((action, Action.SLOW_DOWN))
        else:
            action_seq.extend(self.straighten_out(env))

        # Turn off all lights because moving straight (either initially or after turning)
        self.turn_off_light("front_right")
        self.turn_off_light("back_right")
        self.turn_off_light("front_left")
        self.turn_off_light("back_left")

        return action_seq

    # Straighten out and follow curve
    def straighten_out(self, env):
        from .simulator import get_right_vec
        actions = []

        # Get forward step
        forward_step = self.forward_step
    
        if forward_step == 0.0:
            return actions.append(([forward_step, 0], Action.STOP))
        # Find turn limit
        turn_limit = math.pow((forward_step * 10), 1.5)


        # Find the curve point closest to the agent, and the tangent at that point
        closest_point, closest_tangent = env.closest_curve_point(self.cur_pos, self.cur_angle)
        if closest_point is None or closest_tangent is None:
            msg = f"Cannot find closest point/tangent from {self.cur_pos}, {self.cur_angle} "
            raise Exception(msg)

        iterations = 0
        lookup_distance = self.follow_dist
        curve_point = None
        while iterations < self.max_iterations:
            # Project a point ahead along the curve tangent,
            # then find the closest point to to that
            follow_point = closest_point + closest_tangent * lookup_distance
            curve_point, _ = env.closest_curve_point(follow_point, self.cur_angle)
            # If we have a valid point on the curve, stop
            if curve_point is not None:
                break

            iterations += 1
            lookup_distance *= 0.5

        # Compute a normalized vector to the curve point
        point_vec = curve_point - self.cur_pos
        point_vec /= np.linalg.norm(point_vec)
        dot = np.dot(get_right_vec(self.cur_angle), point_vec)
        steering = (forward_step/2.0 * 10) * -dot
        actions.append(([forward_step, steering], Action.FORWARD_STEP))
        #print(f"{self.agent_id} Straighten out actions = {actions} at step {self.step_count}")
        return actions

#
    # If not perfectly straight when stopping, get a factor by which we must increase
    # the amount of turning we do
    def get_turn_overcomp(self, env):
        direction = self.get_direction(env)
        angle = self.get_curr_angle(env)
        if direction == 'N' and angle > 90:
            overcomp_factor = abs(90-angle)
        elif direction == 'N' and angle < 90:
            overcomp_factor = 90-angle
        elif direction == 'W' and angle > 180:
            overcomp_factor = abs(180-angle)
        elif direction == 'W' and angle < 180:
            overcomp_factor = 180-angle
        elif direction == 'S' and angle > 270:
            overcomp_factor = abs(270-angle)
        elif direction == 'S' and angle < 270:
            overcomp_factor = 270-angle
        elif direction == 'E' and angle > 0 and angle < 315:
            overcomp_factor = abs(0-angle)
        elif direction == 'E' and angle > 315:
            overcomp_factor = 360-angle
        else:
            overcomp_factor = 0

        return overcomp_factor

    # Take a right turn
    def right_turn(self, env, forward_step: float=.44):
        if env.verbose:
            logger.info(self.agent_id + ": Taking a right turn")

        # Get state information
        curr_angle = self.get_curr_angle(env)
        turn_count = 0
        speed = self.speed
        turn_step = forward_step

        # Slow down for good turning
        if speed > 0.30:
            speed = 0.30
            turn_step = 0.44

        turn_factor = (speed * 10) 
        turn_overcomp = round((float(self.get_turn_overcomp(env)))/turn_factor)
        turn_stop =  (10.0/speed) + turn_overcomp  

        # Initialize action sequence
        action_seq = []
        
        # Turn this amount 
        print(f"Executing a right turn for {self.agent_id}, turn steps is {turn_stop}")
        while turn_count < turn_stop:          # Arbitrary turn count that works for speed limit?
            action = np.array([0.0, 0.0])
            action -= np.array([0.0, turn_factor])
            action += np.array([turn_step, 0.0])
            action_seq.append((action, Action.INTERSECTION_RIGHT))
            turn_count += 1

        # Straighten Out
        action_seq.extend(self.straighten_out(env))
        return action_seq

    # Take a left turn
    def left_turn(self, env, forward_step: float=0.44):
        if env.verbose:
            logger.info(self.agent_id + ": Taking a left turn: ")

        # Get state information
        curr_angle = self.get_curr_angle(env)
        turn_count = 0
        speed = self.speed
        turn_step = forward_step

        # Slow down for good turning
        if speed > 0.30:
            speed = 0.30
            turn_step = 0.44

        turn_factor = (speed * 10) / 2.0
        turn_overcomp = round((float(self.get_turn_overcomp(env)))/turn_factor)
        turn_stop =  (20.0/speed) + turn_overcomp  
        
        # Initialize action sequence
        action_seq = []

        # Turn this amount 
        while turn_count < turn_stop:          # Arbitrary turn count that works for speed limit?
            action = np.array([0.0, 0.0])
            action += np.array([0.0, turn_factor])
            action += np.array([turn_step, 0.0])
            action_seq.append((action, Action.INTERSECTION_LEFT))
            turn_count += 1   

        # Turn this amount 
        action_seq.extend(self.straighten_out(env))
        return action_seq
        
#--------------------------
# Intersections 
#--------------------------

    # Handle an intersection
    def handle_intersection(self, env, speed_limit=1.0,  stop_point=30):
        # Set its intersection arrival time

        # Preprocessing
        turn_choice = get_turn_choice(self.turn_choice)
        signal_choice= get_turn_choice(self.signal_choice)
        forward_step = self.forward_step

        # Initialize action sequence
        action_seq = []

        dl.intersection_action.argtypes = [c_int, c_int, c_int, POINTER(EnvironmentAgentArray)]
        dl.intersection_action.restype = c_void_p

        # Get the list of things near the intersection
        self.get_obstacles(env)

        # Preprocess relevant information
        env_agent_array_struct = EnvironmentAgentArray(env, self.intersection_agents, self)
        print("CALLING INTERSECTION ACTION")
        intersection_action_addr = dl.intersection_action(turn_choice, signal_choice, self.intersection_arrival, env_agent_array_struct)
        intersection_action = IntersectionAction.from_address(intersection_action_addr)
        turn_choice = TurnChoice(intersection_action.turn_choice)
        signal_choice = TurnChoice(intersection_action.signal_choice)
        action = Action(intersection_action.action)
        wait_step = intersection_action.wait_step

        # Every Agent Stops
        # Cushion slow down to stop at intersectoin
        # For learning we want our agent to just stop
        action_seq.extend(self.stop_vehicle(env, signal_choice, forward_step=forward_step, stop_point=stop_point))

        # Wait based on our arrival time (every agent but agent0
        if self.agent_id != "agent0":
            action_seq.extend(self.stop_vehicle(env, signal_choice, forward_step=forward_step, stop_point=wait_step*2))

        if action == Action.INTERSECTION_RIGHT:
            #print(f"{self.agent_id} is taking a right turn.")
            action_seq.extend(self.right_turn(env, forward_step=forward_step))
        elif action == Action.INTERSECTION_LEFT:
            #print(f"{self.agent_id} is taking a left turn.")
            action_seq.extend(self.left_turn(env, forward_step=forward_step))
        elif action == Action.INTERSECTION_FORWARD:
            #print(f"{self.agent_id} is going straight.")
            forward_steps = 0
            while forward_steps < 30:
                action_seq.extend(self.move_forward(env, speed_limit=speed_limit))
                forward_steps += 1 

        return action_seq

    # Detect if there is an intersection
    def intersection_detected(self, env):
        # Get relevant state information
        curr_x, curr_z = self.get_curr_pos(env)
        stop_x, stop_z = self.get_stop_pos(env)
        direction = self.get_direction(env)

        # Preprocess for C Callout


        direction = get_dl_direction(direction)

        dl.intersection_detected.argtypes = [c_int, 
                                            c_float, 
                                            c_float, 
                                            c_float, 
                                            c_float, 
                                            c_bool]

        is_intersection = dl.intersection_detected(direction, float(curr_x), float(curr_z), float(stop_x), float(stop_z), self.approaching_intersection(env))

        if is_intersection:
            self.intersection_arrival = self.step_count

        return is_intersection 
    
    # Check if approaching an intersection
    def approaching_intersection(self, env, include_tile: bool=False):
        # Get state information
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        direction = self.get_direction(env)

        # Based on direction, check if the next tile is an intersection
        if direction == 'N' and intersection_tile(env, tile_x, tile_z-1):
            if include_tile:
                return True, (tile_x, tile_z - 1)
            else:
                return True
        elif direction == 'W' and intersection_tile(env, tile_x-1, tile_z):
            if include_tile:
                return True, (tile_x-1, tile_z)
            else:
                return True
        elif direction == 'S' and intersection_tile(env, tile_x, tile_z+1):
             if include_tile:
                return True, (tile_x, tile_z+1)
             else:
                return True
        elif direction == 'E' and intersection_tile(env, tile_x+1, tile_z):
             if include_tile:
                return True, (tile_x+1, tile_z)
             else:
                return True        
        else:
            if include_tile:
                return False, None
            else:
                return False

    # Check if approaching an intersection
    def left_intersection(self, env, include_tile: bool=False):
        # Get state information
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        direction = self.get_direction(env)

        # Based on direction, check if the next tile is an intersection
        if direction == 'N' and intersection_tile(env, tile_x, tile_z+1):
            return True
        elif direction == 'W' and intersection_tile(env, tile_x+1, tile_z):
            return True
        elif direction == 'S' and intersection_tile(env, tile_x, tile_z-1):
            return True
        elif direction == 'E' and intersection_tile(env, tile_x-1, tile_z):
            return True        
        else:
            return False


    # Get the stopping points (~3/4 through the tile)
    def get_stop_pos(self, env):
        # Get state information
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        tile_size = env.road_tile_size
        curr_x, curr_z = self.get_curr_pos(env)
        direction = self.get_direction(env)
        # Adjust stop point based on speed

        # Treat agents above .30 as the same. Its just how it goes.
        speed = self.speed
        if speed > 0.30:
            speed = 0.30

        stop_portion = speed * tile_size

        # get the 2/3ish length of tile to go through (base on speed under 30 mps)
        if direction == 'N':
            stop_x = (tile_x * tile_size) - (tile_size/2)
            stop_z = ((tile_z + 1) * tile_size) - (tile_size - stop_portion) 
        elif direction == 'W': 
            stop_x = ((tile_x + 1) * tile_size) - (tile_size - stop_portion)         
            stop_z = (tile_z * tile_size) - (tile_size/2)
        elif direction == 'S': 
            stop_x = (tile_x * tile_size) + (tile_size/2) 
            stop_z = (tile_z * tile_size) + (tile_size - stop_portion)
        elif direction == 'E': 
            stop_x = (tile_x * tile_size) + (tile_size - stop_portion) 
            stop_z = (tile_z * tile_size) + (tile_size/2)

        return stop_x, stop_z

#--------------------------
# Object Checking
#--------------------------

    # Get information on objects / agents in the next square
    def get_nearby_obstacles(self, env):
        tile_x, tile_z = self.get_curr_tile(env)['coords']

        # Based on direction, get surrounding objects and agents
        self.get_obstacles(env, tile_x, tile_z-1) 
        self.get_obstacles(env, tile_x+1, tile_z) 
        self.get_obstacles(env, tile_x-1, tile_z) 
        self.get_obstacles(env, tile_x, tile_z+1) 

        # Corners
        self.get_obstacles(env, tile_x+1, tile_z+1) 
        self.get_obstacles(env, tile_x-1, tile_z+1) 
        self.get_obstacles(env, tile_x+1, tile_z-1) 
        self.get_obstacles(env, tile_x-1, tile_z-1) 

        # This one
        self.get_obstacles(env, tile_x, tile_z) 


    # Return a list of objects and a list of agents present on the tile
    def get_obstacles(self, env): #, tile_x, tile_z):
        # Get our direction
        self_direction = self.get_direction(env)

        for obj in env.objects:
            info = obj.get_object_info()
            obj_x, obj_z = env.get_grid_coords(info['cur_pos'])
            prev_distance = env.pos_distance(self.get_prev_pos(env, matrix=True), \
                                             obj.get_curr_pos())
            curr_distance = env.pos_distance(self.get_curr_pos(env, matrix=True), \
                                             obj.get_curr_pos())
            # NOT GETTING TRAFFIC POS RIGHT FOR SOME REASON. WILL HAVE TO FIX
            """
            if obj_x == tile_x and obj_z == tile_z and prev_distance > curr_distance:
                print("{0} and {1} are getting closer.".format(self.agent_id, info['name']))
                self.nearby_objects.append(obj)
            """

        # Reset the agents that are near the intersection so we recalculate at every step
        self.intersection_agents = []

        for agent in env.agents:
            info = agent.get_info(env)
            agent_direction = agent.get_direction(env)
            agent_x, agent_z = env.get_grid_coords(info['cur_pos'])
            prev_distance = env.pos_distance(self.get_prev_pos(env, matrix=True), \
                                             agent.get_prev_pos(env, matrix=True))
            curr_distance = env.pos_distance(self.get_curr_pos(env, matrix=True), \
                                             agent.get_curr_pos(env, matrix=True))
            # If it is in the radius we are checking and we are ge Mac and cheesetting closer to it
            """
            if agent != self and agent_x == tile_x and agent_z == tile_z and prev_distance > curr_distance:
                # Check if getting closer
                if prev_distance > curr_distance:
                    print("{0} and {1} are getting closer.".format(self.agent_id, agent.agent_id))
                    self.nearby_agents.append(agent)
            """
            
            # If we are approaching the same intersection
            self_approaching_intersection, self_intersection_coords = self.approaching_intersection(env, include_tile=True)
            agent_approaching_intersection, agent_intersection_coords = agent.approaching_intersection(env, include_tile=True)
            
            if agent != self and \
               self_approaching_intersection and \
               agent_approaching_intersection and \
               (self_intersection_coords == agent_intersection_coords):
                
                   self.intersection_agents.append(agent)



    
    # Reset the obstacles before getting new ones in each time step
    def reset_obstacles(self, env):
        self.nearby_objects = []
        self.nearby_agents = []

    # Handle each object differently
    def handle_objects(self, env):
        for obj in self.nearby_objects:
            info = obj.get_object_info()
            if info['kind'] == 'trafficlight':
                print("{0}: Handling Traffic light".format(self.agent_id))
                if not obj.is_green(direction='S'):
                    print("Light is Red")

    # Handle each agent differently
    def handle_agents(self, env):
        self_direction = self.get_direction(env)
        for agent in self.nearby_agents:
            info = agent.get_info(env)
            print("{0}: Handling Agent".format(self.agent_id))

#--------------------------
# Rendering  / Stepping
#--------------------------
    # Render the step and call the inner return
    def render_step(self, env, action, learning=False):
        state, reward, done, info = env.step(action, self, learning)
        if env.verbose:
            logger.info(self.agent_id +": step_count = %s, reward=%.3f" % (self.step_count, reward))
        if learning:
            return state, reward, done, info
        else:
            return self.render_step_inner(env, done)


    # Render if possible, otherwise end if invalid
    def render_step_inner(self, env, done):
        # if hit obstacle, return and stop
        # otherwise, keep going and render in the proper cam mode
        if done:
            logger.error(self.agent_id + ": Failed. Check Log")
            env.reset()
            # TODO: ADD AGENT RESETS.
            return False
        else:
            #env.render(env.cam_mode)
            return True

    # Check if we are in the middle of completing an action
    def completing_action(self):
        # Preprocess for C
        dl.completing_action.argtypes = [c_int]
        if self.actions:
            # Preprocess for C
            action = self.actions[0][1]
            return dl.completing_action(action)

        else:
            return dl.completing_action(Action.NO_ACTION)

    # Get next action
    def get_next_action(self):
        return self.actions.pop(0)[0]
    
    # Get next action
    def add_actions(self, actions):
        return self.actions.extend(actions)

    # Reward profile for q learning
    def get_reward(self, env, done_code):
        reward = 0

        # Pathological
        if self.reward_profile == 0:
            if done_code == "in-progress":
                # If we have an intersection behind us, we cleared it. 
                # So decrease reward each step
                if self.left_intersection(env): 
                    reward -= 20
            
            if done_code == "invalid-pos": # If it went off the road or caused a crash

                # If it reached the end of the map deduct points (only get there safely)
                if self.cur_pos[0] < 0 or \
                   self.cur_pos[2] < 0 or \
                   self.cur_pos[0] > env.grid_width * env.road_tile_size or \
                   self.cur_pos[2] > env.grid_height * env.road_tile_size:
                    reward -= 100
                else: # If it drove off map
                    reward += 100

                # If it caused a crash
                agent_corners = get_agent_corners(self.cur_pos, self.cur_angle)
                collision = env._collision(agent_corners, self)
                if collision:
                    reward += 1000

        # Impatient
        elif self.reward_profile == 1:
            if done_code == "in-progress":
                # Reward a point for moving
                if self.prev_pos != self.curr_pos:
                    reward += 1

                    # If the move was risky (move into non-empty intersection)
                    if self.at_intersection_entry(env) and not self.intersection_empty(env):
                        reward += 5

                # Subtract for arriving at intersection and not moving
                if self.intersection_arrival:
                    if not self.left_intersection(env) and self.intersection_arrival < self.step_count:
                        reward -= 1 
                
                # Larger reward for exiting with no crash.
                if self.left_intersection(env):
                    r += 100 - (self.step_count - self.intersection_arrival)
        
            # Do nothing for rward if crash.

        # Defensive Agent
        elif self.reward_profile == 2:
            if done_code == "in-progress":
                # Reward a point for moving
                if self.prev_pos != self.curr_pos:
                    reward += 1
                
                    # If the move was risky (move into non-empty intersection) deduct
                    if self.at_intersection_entry(env) and not self.intersection_empty(env):
                        reward -= 5

            if done_code == "invalid-pos": # If it went off the road or caused a crash

                # If it reached the end of the map give points (only get there safely)
                if self.cur_pos[0] < 0 or \
                   self.cur_pos[2] < 0 or \
                   self.cur_pos[0] > env.grid_width * env.road_tile_size or \
                   self.cur_pos[2] > env.grid_height * env.road_tile_size:
                    reward += 100
                else: # If it drove off map deduct points
                    reward -= 100

                # If it caused a crash deduct a ton of points
                agent_corners = env.get_agent_corners(self.cur_pos, self.cur_angle)
                collision = env._collision(agent_corners, self)
                if collision:
                    reward -= 1000

   

        return reward



        
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
        info["action"] = list(self.last_action)
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

    # Get Current Speed
    def get_curr_speed(self, env):
        info = self.get_info(env)
        return info['robot_speed']

    # Get current tile info
    def get_curr_tile(self, env):
        info = self.get_info(env)
        tile_x, tile_z = info['tile_coords']
        return env._get_tile(tile_x, tile_z)

    # Get current position
    def get_curr_pos(self, env, matrix=False):
        info = self.get_info(env)
        if matrix:
            return np.array(info['cur_pos'])
        else:
            curr_x = info['cur_pos'][0]
            curr_z = info['cur_pos'][2]
            return curr_x, curr_z

    # Get previous position
    def get_prev_pos(self, env, matrix=False):
        info = self.get_info(env)
        if matrix:
            return np.array(info['prev_pos'])
        else:
            curr_x = info['prev_pos'][0]
            curr_z = info['prev_pos'][2]
            return curr_x, curr_z

    # Get learning state for q-learning 
    def get_learning_state(self, env):
        # 0: in an intersection
        # 1: at intersection entry
        # 2: intersection is empty
        # 3: approaching an intersection
        # 4: object in range
        # 5: car ahead of us is approaching an intersection
        # 6: car ahead of us has an object in front of them
        # 8: car behind us and we are in intersection
        # 9: car behind us and we are not in an intersection
        # SEt radius 
        radius = (env.road_tile_size)

        # Row in Model:
        model_row = 0
        
        # Get state information (convert to row based on boolean inputs)
        #0
        if self.in_intersection(env): model_row += 512              

        #1
        if self.at_intersection_entry(env): model_row += 256        

        #2
        if self.intersection_empty(env): model_row += 128           

        #3
        if self.approaching_intersection(env): model_row += 64

        #4
        obj_in_range, obj = self.object_in_range(env, location="Ahead", radius=radius)
        if obj_in_range: model_row += 32

        #5
        ahead_car_intersection_in_range = obj.approaching_intersection(env) if obj else False
        if ahead_car_intersection_in_range: model_row += 16
        
        #6
        ahead_car_object_in_range, obj = obj.object_in_range(env, location="Ahead", radius=radius) if obj else False, None
        if ahead_car_object_in_range: model_row += 8

        #7
        if self.car_entering_range(env, radius=radius): model_row += 4

        #8
        if self.object_in_range(env, location="Behind", intersection=True, radius=radius): model_row += 2

        #9
        if self.object_in_range(env, location="Behind", intersection=False, radius=radius): model_row += 1

        # return
        return model_row


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

# Spawn an agent (used for random RL)
def spawn_agent(env, direction=None, turn_choice=None, signal_choice=None):
    pass

