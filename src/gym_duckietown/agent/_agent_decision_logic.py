from ..dl_utils import *
from learn_types import *
import numpy as np
import os
from ..agents import so_file, dl
from ._agent_utils import intersection_tile
import math

#--------------------------
# Decision Logic
#--------------------------

def proceed(self, env, good_agent=False, learning=False, model=None, state=None):

    # If we are good we want to avoid tailgating
    if good_agent:
        if self.is_tailgating(env):
            self.handle_proceed(False)
            #print(f"{self.agent_id} {self.color} {self.get_direction(env)} is forced to stop for tailgating")
            return 
        
        if not self.has_right_of_way(env):
            self.handle_proceed(False)
            #print(f"{self.agent_id} {self.color} {self.get_direction(env)} is forced to stop no right of way")
            return 

        # Else Remove Stop
        self.handle_proceed(True)
        return

    # Call out to c with the model and the state and see what we should do, then handle it.
    elif learning:
        dl.proceed.argtypes = [QTable, c_int]
        dl.proceed.restype = c_bool

        should_proceed = dl.proceed(model, state)
        self.handle_proceed(should_proceed)

# Handle wheather or not we should proceed.
def handle_proceed(self, should_proceed):
    if not should_proceed:
        no_intersection_stop_actions = []
        # if we are not stopping anyways, append a stop.
        if self.actions[0][1] != Action.INTERSECTION_STOP and self.actions[0][1] != Action.STOP:
            action = np.array([0.0, 0.0])
            self.actions = [(action, Action.STOP)] + no_intersection_stop_actions
    

    elif should_proceed:
        no_stop_actions = []
        for action in self.actions:
            if action[1] != Action.STOP:
                no_stop_actions.append(action)

        self.actions = no_stop_actions

# Check if we have the right of way
def has_right_of_way(self, env):
    # Create a list of agents who are at the intersection or in it.
    n_agents = []
    s_agents = []
    e_agents = []
    w_agents = []
    other_in_intersection = False
    for agent in env.agents:
        if agent != self:
            # We don't have right of way if someone else is in the intersection
            if agent.in_intersection(env):
                other_in_intersection = True
            elif agent.at_intersection_entry(env):
                if agent.get_direction(env) == 'N':
                    n_agents.append(agent)
                elif agent.get_direction(env) == 'S':
                    s_agents.append(agent)
                elif agent.get_direction(env) == 'E':
                    e_agents.append(agent)
                elif agent.get_direction(env) == 'W':
                    w_agents.append(agent)

    # If more than one car is at intersection, wait till we have right of way (Rightmost Counter Clockwise)
    # Intersection Priority: Rightmost counter clockwise. For two going same direction, N/S tiebreaker is N, 
    # E/W tiebreaker is W heading agent
    dl.has_right_of_way.argtypes = [c_bool, c_bool, c_bool, c_int, c_bool, c_bool, c_bool, c_bool]
    dl.has_right_of_way.restype = c_bool

    # Call out to c decision logic
    row = dl.has_right_of_way(self.in_intersection(env), other_in_intersection, self.at_intersection_entry(env), get_dl_direction(self.get_direction(env)), bool(n_agents), bool(s_agents), bool(e_agents), bool(w_agents))
    #print(f"{self.agent_id} right of way {row}")
    return row
        

# Check if we are at an intersection
def in_intersection(self, env):
    if self.in_bounds(env):
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        return intersection_tile(env, tile_x, tile_z)
    else:
        return False

# Check if we are at an intersection
def at_intersection_entry(self, env):
    # Get state information
    if self.in_bounds(env):
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
                if self.cur_pos[2] > stop_line - env.robot_length/3 and self.cur_pos[2] < stop_line + env.robot_length:
                    return True
            elif direction == 'S':
                stop_line = (intersection_coords[1] + 0 if intersection_coords[1] != 0 else 1) * env.road_tile_size
                if self.cur_pos[2] < stop_line + env.robot_length/3 and self.cur_pos[2] > stop_line - env.robot_length:
                    return True
            elif direction == 'E':
                stop_line = (intersection_coords[0] + 0 if intersection_coords[0] != 0 else 1) * env.road_tile_size
                if self.cur_pos[0] < stop_line + env.robot_length/3 and self.cur_pos[0] > stop_line - env.robot_length:
                    return True
            elif direction == 'W':
                stop_line = (intersection_coords[0] + 1) * env.road_tile_size
                if self.cur_pos[0] > stop_line - env.robot_length/3 and self.cur_pos[0] < stop_line + env.robot_length:
                    return True
            else:
                return False
    else: 
        return False

# Check if approaching intersection and another car is at entry or approaching and if it arrived before i did. Only return
# if it is still completing the intersection. otherwise, its fine.
def cars_arrived_before_me(self, env):
    cars_before_me = []
    for agent in env.agents:
        if agent != self:
            # If intersection_detected intersection, not at entry and agent is and we 
            #if (self.intersection_detected(env) or self.approaching_intersection(env)) and not self.at_intersection_entry(env) and agent.at_intersection_entry(env):
            if agent.intersection_arrival and self.intersection_arrival and agent.intersection_arrival < self.intersection_arrival:
                if agent.at_intersection_entry(env) or agent.in_intersection(env) or agent.approaching_intersection(env):
                    cars_before_me.append(agent)
    
    return cars_before_me

# check and see if a car is waiting to enter.
def cars_waiting_to_enter(self, env):
    cars_waiting_to_enter = []
    for agent in env.agents:
        if agent != self:
            if agent.at_intersection_entry(env) and self.in_intersection(env):
                cars_waiting_to_enter.append(agent)
    
    return cars_waiting_to_enter


# Check if anyone other than us is currently in the intersection
def intersection_empty(self, env):
    if self.in_bounds(env):
        tile_x, tile_z = 2,2
        intersection_empty = True
        for agent in env.agents:
            if not agent.get_curr_tile(env):
                continue
            agent_tile_x, agent_tile_z = agent.get_curr_tile(env)['coords']
            if agent_tile_x == tile_x and agent_tile_z == tile_z and agent != self:
                intersection_empty = False
        return intersection_empty
    else:
        return False


# See if there is an object within one tile block of a car infront of us
def object_in_range(self, env, location="Ahead", intersection=None, radius=1, return_multiple=False, forward_only=False):
    if self.in_bounds(env):
        tile_x, tile_z = self.get_curr_tile(env)['coords']
        direction = self.get_direction(env)
        if forward_only:
            side_radius = radius / 3
        else:
            side_radius = radius / 4
        front_radius = radius

        if direction == 'N':
            # Lower bound for xrange is our current x minus half a tile
            # Upper bound for xrange is our current x plus half a tile
            # Lower bound for zrange is our current z - tilesize
            # Upper bound for zrange is our current z
            if location == "Ahead":
                object_ahead_range_z_lb = self.cur_pos[2] - front_radius
                object_ahead_range_z_ub = self.cur_pos[2] 
            elif location == "Behind":
                object_ahead_range_z_lb = self.cur_pos[2] + env.robot_length
                object_ahead_range_z_ub = self.cur_pos[2] + front_radius + env.robot_length
            object_ahead_range_x_lb = self.cur_pos[0] - side_radius
            object_ahead_range_x_ub = self.cur_pos[0] + side_radius 
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
            if agent.agent_id != self.agent_id and location == "Ahead":
                if agent_x >= object_ahead_range_x_lb and agent_x <= object_ahead_range_x_ub and \
                agent_z >= object_ahead_range_z_lb and agent_z <= object_ahead_range_z_ub:
                    if self.agent_id == "agent0":
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
    else:
        return False, None

def is_tailgating(self, env):
    for agent in env.agents:
        #print(f"Comparing Agent {self} to {agent}")
        #print(f"Comparing Agent {self.agent_id} {self.color} to {agent.agent_id} {agent.color}")
        if agent.agent_id != self.agent_id:
            info = agent.get_info(env)
            agent_direction = agent.get_direction(env)
            agent_x, agent_z = env.get_grid_coords(info['cur_pos'])
            prev_distance = env.pos_distance(self.prev_pos, agent.prev_pos)
            curr_distance = env.pos_distance(self.cur_pos, agent.cur_pos)
            if  agent_direction == self.get_direction(env) and \
                prev_distance > curr_distance and \
                curr_distance < env.robot_length*3 and \
                self.is_behind(env, agent):

                #print(f"Agent {self.color} is tailgating {agent.color}")
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