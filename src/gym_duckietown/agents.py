from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union
from .objmesh import get_mesh, MatInfo, ObjMesh
import numpy as np
import random
import numpy as np
import math
from . import logger
from gym_duckietown import objects

"""
Contains functions for moving agent in ite world scenarios.
"""
class Agent():
    cur_pos: np.ndarray
    cur_angle: np.ndarray
    last_action: np.ndarray
    actions: List[np.ndarray]
    wheelsVels: np.ndarray
    step_count: int
    start_tile: List[int] 
    start_pose: List[Union[List[Union[float, int]], Union[float, int]]] 
    speed: float 
    color: str 
    timestamp: float 
    agent_id: str 
    nearby_objects: List[objects.WorldObj]         # Keep track of nearby objects and agents
    nearby_agents: List
    follow_dist: float
    max_iterations: int

    def __init__(self,
        cur_pos=[0.0, 0.0, 0.0],
        cur_angle=0.0,
        start_tile=(0, 0),
        start_pose=[[0.0, 0.0, 0.0], 0.0],
        agent_id="ID",
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
        self.mesh = get_duckiebot_mesh(color)
        self.nearby_objects = []          # Keep track of nearby objects and agents
        self.nearby_agents = []
        self.actions = []
        self.step_count = 0
        self.follow_dist = 0.3
        self.max_iterations = 1000
        height = 0.05
        self.lights =   {
                        "front_left": [0.1, -0.05, height, False],
                        "front_right": [0.1, +0.05, height, False],
                        "center": [0.1, +0.0, height, False],
                        "back_left": [-0.1, -0.05, height, False],
                        "back_right": [-0.1, +0.05, height, False],
                        }

#--------------------------
# Lights
#--------------------------

    # Turn on Specific Light
    def turn_on_light(self, light):
        self.lights[light][3] = True

    # Turn off Specific Light
    def turn_off_light(self, light):
        self.lights[light][3] = False

    # Stop the vehicle
    def stop_vehicle(self, env, choice, wrong_light: bool=False, stop_point: int=30,forward_step: float=0.44):
        if env.verbose:
            logger.info(self.agent_id + ": Stopping")
        stop_iterations = 0

        # Initialize action sequence
        action_seq = []

        # While still moving Slow down
        while stop_iterations < stop_point:
            action = np.array([0.0, 0.0])
            action_seq.append(action)
            # Turn on respective turn signals
            if choice == "Right" and not wrong_light:
                self.turn_on_light("front_right")
                self.turn_on_light("back_right")
            elif choice == "Left" and not wrong_light:
                self.turn_on_light("front_left")
                self.turn_on_light("back_left")
            elif choice == "Right" and wrong_light:
                self.turn_on_light("front_left")
                self.turn_on_light("back_left")
            elif choice == "Left" and wrong_light:
                self.turn_on_light("front_right")
                self.turn_on_light("back_right")
            stop_iterations += 1

        return action_seq

    
#--------------------------
# Movement
#--------------------------

    # Move Forwards at whatever angle we are at, not going faster than 30 mps
    def move_forward(self, env, forward_step=0.44, speed_limit=1.0):
        # Get state information
        curr_speed = self.get_curr_speed(env)
        if env.verbose:
            logger.info(self.agent_id + ": Moving Forwards at speed " + str(curr_speed))

        # Initialize action sequence
        action_seq = []

        # While still moving Slow down
        if curr_speed > speed_limit:
            action = np.array([0.0, 0.0])
            action_seq.append(action)
        else:
            action_seq.extend(self.straighten_out(env, forward_step=forward_step))

        # Turn off all lights because moving straight (either initially or after turning)
        self.turn_off_light("front_right")
        self.turn_off_light("back_right")
        self.turn_off_light("front_left")
        self.turn_off_light("back_left")

        return action_seq

    # Straighten out and follow curve
    def straighten_out(self, env, forward_step: float=0.44):
        from .simulator import get_right_vec
        actions = []
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
        actions.append([forward_step, steering])
        return actions

    # TO DO LATER TO SEPARATE NP Python STUFF FROM C CALLBACKS
    def get_curve_point(self):
        print("NOTHING")
    

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
        while turn_count < turn_stop:          # Arbitrary turn count that works for speed limit?
            action = np.array([0.0, 0.0])
            action -= np.array([0.0, turn_factor])
            action += np.array([turn_step, 0.0])
            action_seq.append(action)
            turn_count += 1

        # Straighten Out
        action_seq.extend(self.straighten_out(env, forward_step=forward_step))
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
            action_seq.append(action)
            turn_count += 1   

        # Turn this amount 
        action_seq.extend(self.straighten_out(env, forward_step=forward_step))
        return action_seq
        
#--------------------------
# Intersections 
#--------------------------

    # Handle an intersection
    # wrong_light=False, so agent behaves good and turns on correct signal lights
        # wrong_light=True, agent behaves bad and turns on wrong signal lights
    def handle_intersection(self, env, forward_step=.44, speed_limit=1.0, choice=None, wrong_light=False, stop_point=30):

        # Initialize action sequence
        action_seq = []

        # Choose a random option if one not given
        choices = ['Right', 'Left', 'Straight'] 
        if choice == None:
            choice = random.choice(choices)

        # Stop
        action_seq.extend(self.stop_vehicle(env, choice, wrong_light=wrong_light, forward_step=forward_step, stop_point=stop_point))

        if choice == 'Right':
            action_seq.extend(self.right_turn(env, forward_step=forward_step))
        elif choice == 'Left':
            action_seq.extend(self.left_turn(env, forward_step=forward_step))
        else:
            forward_steps = 0
            while forward_steps < 30:
                action_seq.extend(self.move_forward(env, forward_step=forward_step, speed_limit=speed_limit))
                forward_steps += 1 

        return action_seq

    # Detect if there is an intersection
    def intersection_detected(self, env):
        # Get relevant state information
        curr_x, curr_z = self.get_curr_pos(env)
        stop_x, stop_z = self.get_stop_pos(env)
        direction = self.get_direction(env)

        # Based on direction check intersection
        if direction == 'N' and curr_z < stop_z and self.approaching_intersection(env):
            return True
        elif direction == 'W' and curr_x < stop_x and self.approaching_intersection(env):
            return True
        elif direction == 'S' and curr_z > stop_z and self.approaching_intersection(env):
            return True
        elif direction == 'E' and curr_x > stop_x and self.approaching_intersection(env):
            return True
        else:
            return False

    # Check if approaching an intersection
    def approaching_intersection(self, env):
        # Get state information
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        direction = self.get_direction(env)
        print(self.agent_id, direction, self.cur_pos, tile_x, tile_z)

        # Based on direction, check if the next tile is an intersection
        if direction == 'N' and intersection_tile(env, tile_x, tile_z-1):
            return True
        elif direction == 'W' and intersection_tile(env, tile_x-1, tile_z):
            return True
        elif direction == 'S' and intersection_tile(env, tile_x, tile_z+1):
            return True
        elif direction == 'E' and intersection_tile(env, tile_x+1, tile_z):
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
    def get_obstacles(self, env, tile_x, tile_z):
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
            if obj_x == tile_x and obj_z == tile_z and prev_distance > curr_distance:
                print("{0} and {1} are getting closer.".format(self.agent_id, info['name']))
                self.nearby_objects.append(obj)

        for agent in env.agents:
            info = agent.get_info(env)
            agent_direction = agent.get_direction(env)
            agent_x, agent_z = env.get_grid_coords(info['cur_pos'])
            prev_distance = env.pos_distance(self.get_prev_pos(env, matrix=True), \
                                             agent.get_prev_pos(env, matrix=True))
            curr_distance = env.pos_distance(self.get_curr_pos(env, matrix=True), \
                                             agent.get_curr_pos(env, matrix=True))
            # If it is in the radius we are checking and we are ge Mac and cheesetting closer to it
            if agent != self and agent_x == tile_x and agent_z == tile_z and prev_distance > curr_distance:
                # Check if getting closer
                if prev_distance > curr_distance:
                    print("{0} and {1} are getting closer.".format(self.agent_id, agent.agent_id))
                    self.nearby_agents.append(agent)
    
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
    def render_step(self, env, action):
        obs, reward, done, info = env.step(action, self)
        if env.verbose:
            logger.info(self.agent_id +": step_count = %s, reward=%.3f" % (self.step_count, reward))
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

    # Get next action
    def get_next_action(self):
        return self.actions.pop(0)
    
    # Get next action
    def add_actions(self, actions):
        return self.actions.extend(actions)
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

