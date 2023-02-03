from ..dl_utils import *
from learn_types import *
import numpy as np
from ..agents import dl
import time

#--------------------------
# Decision Logic
# Contains much of the information gathering for agent state, and how to decide what to do.
#--------------------------

# Have an agent proceed, using a model, unless it is a naturally good agent
def proceed(self, env, good_agent=False, use_model=False, model=None, state=None):

    # TEST FOR THE C DECISION LOGIC THAT EVERYTHING IS NICE!    
    #dl.print_all.argtypes = [POINTER(EnvironmentInfo)]
    #dl.print_all.restype = c_void_p

    # Preprocess relevant information
    #dl.print_all(env.c_info_struct)
    # If we are good we want to avoid tailgating
    if good_agent:
        dl.proceed_good_agent.argtypes = [POINTER(EnvironmentInfo), c_int]
        dl.proceed_good_agent.restype = c_bool
        proceed = dl.proceed_good_agent(env.c_info_struct, self.index)
        self.handle_proceed(env, proceed)

        dl.handle_patience.argtypes = [POINTER(EnvironmentInfo), c_int]
        dl.handle_patience.restype = c_int
        
        handle_patience_ret = dl.handle_patience(env.c_info_struct, self.index)
        if handle_patience_ret == 1:
            self.patience += 1
        elif handle_patience_ret == 2:
            self.patience = 0

        return 

    # Call out to c with the model and the state and see what we should do, then handle it.
    elif use_model:
        dl.proceed_model.argtypes = [QTable, c_int]
        dl.proceed_model.restype = c_bool

        should_proceed = dl.proceed_model(model, state)
        self.handle_proceed(env, should_proceed)

# Handle whether or not we should proceed, filter out bad actions
def handle_proceed(self, env, should_proceed):
    if not should_proceed:
        no_intersection_stop_actions = []

        # if we are not stopping anyways, append a stop.
        if not self.actions or (self.actions[0][1] != Action.INTERSECTION_STOP and self.actions[0][1] != Action.STOP):
            action = np.array([0.0, 0.0])
            self.actions = [(action, Action.STOP)] + no_intersection_stop_actions
            # Turn on break lights
        self.turn_on_light('back_right')
        self.turn_on_light('back_left')
        if self.actions:
            if self.actions[0][1] == Action.INTERSECTION_FORWARD or \
               self.states['in_intersection'] or self.states['at_intersection_entry']:
                self.turn_off_all_lights()
                self.signal_for_turn(self.signal_choice)
            if self.actions[0][1] == Action.INTERSECTION_STOP or \
               self.actions[0][1] == Action.STOP:
                self.turn_on_light('back_right')
                self.turn_on_light('back_left')
            if self.actions[0][1] == Action.FORWARD_STEP:
                self.turn_off_all_lights()
                if self.states['in_intersection'] or self.states['at_intersection_entry']:
                    self.signal_for_turn(self.signal_choice)

    elif should_proceed:
        no_stop_actions = []
        for action in self.actions:
            # If we have a stop move, take it out
            if action[1] != Action.STOP:
                no_stop_actions.append(action)
            

        self.actions = no_stop_actions

        if self.actions:
            if self.actions[0][1] == Action.INTERSECTION_FORWARD or \
               self.states['in_intersection'] or self.states['at_intersection_entry']:
                self.turn_off_all_lights()
                self.signal_for_turn(self.signal_choice)
            if self.actions[0][1] == Action.INTERSECTION_STOP or \
               self.actions[0][1] == Action.STOP:
                self.turn_on_light('back_right')
                self.turn_on_light('back_left')
            if self.actions[0][1] == Action.FORWARD_STEP:
                self.turn_off_all_lights()
                if self.states['in_intersection'] or self.states['at_intersection_entry']:
                    self.signal_for_turn(self.signal_choice)

            #if self.states['in_intersection']:
            #    self.intersection_arrival = -1

            """
            prev_tile_x, prev_tile_z = env.get_grid_coords(self.prev_pos)
            tile_x, tile_z = env.get_grid_coords(self.prev_pos)
            prev_tile = env._get_tile(prev_tile_x, prev_tile_z)
            cur_tile = env._get_tile(tile_x, tile_z)
            if prev_tile and cur_tile:
                if prev_tile['kind'] == '4way' and cur_tile['kind'] != '4way':
                    self.intersection_arrival = -1
            """

        if not self.actions:
            self.actions = [()]


# Check if we are next in line to go in ROW
def next_to_go(self, env):
    # C callout
    dl.next_to_go.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.next_to_go.restype = c_bool
    return dl.next_to_go(env.c_info_struct, int(self.index))

# Check if we have the right of way
def has_right_of_way(self, env):
    # If more than one car is at intersection, wait till we have right of way (Rightmost Counter Clockwise)
    # Intersection Priority: Rightmost counter clockwise. For two going same direction, N/S tiebreaker is N, 
    # E/W tiebreaker is W heading agent

    # C decision logic
    dl.has_right_of_way.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.has_right_of_way.restype = c_bool
    return dl.has_right_of_way(env.c_info_struct, int(self.index))
        
# Check if we have the right of way
def safe_to_enter(self, env):
    dl.safe_to_enter.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.safe_to_enter.restype = c_bool
    return dl.safe_to_enter(env.c_info_struct, int(self.index))

# Check if we are at an intersection
def in_intersection(self, env):
    # C callout
    dl.in_intersection.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.in_intersection.restype = c_bool
    in_intersection = dl.in_intersection(env.c_info_struct, int(self.index))
    return in_intersection

# Check if we are at an intersection entry (right at the line)
def at_intersection_entry(self, env):
    # c callout
    dl.at_intersection_entry.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.at_intersection_entry.restype = c_bool
    return dl.at_intersection_entry(env.c_info_struct, int(self.index))

# Check if approaching intersection and another car is at entry or approaching and if it arrived before i did. Only return
# if it is still completing the intersection. otherwise, its fine.
def cars_arrived_before_me(self, env):
    # c callout
    dl.cars_arrived_before_me.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.cars_arrived_before_me.restype = c_bool
    return dl.cars_arrived_before_me(env.c_info_struct, int(self.index))

# check and see if a car is waiting to enter.
def cars_waiting_to_enter(self, env):
    # c callout
    dl.cars_waiting_to_enter.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.cars_waiting_to_enter.restype = c_bool
    return dl.cars_waiting_to_enter(env.c_info_struct, int(self.index))

# Check if anyone other than us is currently in the intersection
def intersection_empty(self, env):
    # c callout
    dl.intersection_empty.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.intersection_empty.restype = c_bool
    return dl.intersection_empty(env.c_info_struct, int(self.index))


# See if there is an object within one tile block of a car infront of us
def object_in_range(self, env, location="Ahead", intersection=None, radius=1, return_multiple=False):
    # Location = 1 for ahead, 2 for behind
    # C cal1lout
    location_param = 0
    if location == 'Ahead':
        location_param = 1
    elif location == 'Behind':
        location_param = 2

    dl.object_in_range.argtypes = [POINTER(EnvironmentInfo), c_int, c_int]
    dl.object_in_range.restype = c_bool
    return dl.object_in_range(env.c_info_struct, int(self.index), int(location_param))

# Check if we are tailgating
def is_tailgating(self, env):
    # C callout
    dl.is_tailgating.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.is_tailgating.restype = c_bool
    return dl.is_tailgating(env.c_info_struct, int(self.index))

# Check if we are behind another agent
def is_behind(self, env):
    # C cal1lout
    dl.is_behind.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.is_behind.restype = c_bool
    return dl.is_behind(env.c_info_struct, int(self.index))

# See if a car is entering out range
def car_entering_range(self, env, radius=1):
    # C cal1lout
    dl.car_entering_range.argtypes = [POINTER(EnvironmentInfo), c_int, c_int]
    dl.car_entering_range.restype = c_bool
    return dl.car_entering_range(env.c_info_struct, int(self.index), int(1)) # location ahead

# Get current direction
def get_direction(self, env):
    # C callout
    dl.get_direction.argtypes = [c_float]
    dl.get_direction.restype = c_char
    return dl.get_direction(float(self.get_curr_angle(env))).decode('utf-8')
    
    
# Check if agent is in bounds
def in_bounds(self, env):
    # C callout
    dl.in_bounds.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.in_bounds.restype = c_bool
    return dl.in_bounds(env.c_info_struct, int(self.index))

# Check if a tile is an intersection tile
def intersection_tile(env, tile_x, tile_z):

    # C Callout
    dl.intersection_tile.argtypes = [POINTER(EnvironmentInfo), c_int, c_int]
    dl.intersection_tile.restype = c_bool
    return dl.intersection_tile(env.c_info_struct, int(tile_x), int(tile_z))

# Get learning state for q-learning 
def get_learning_state(self, env):
    # C callout to get model number
    dl.get_learning_state.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.get_learning_state.restype = c_int
    model_row =  dl.get_learning_state(env.c_info_struct, int(self.index))
    pre_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    state_size = 10
    state = [int(i) for i in list('{0:0b}'.format(model_row))]
    state = pre_state[0:state_size - len(state)] + state
    state = [bool(i) for i in state]
    
    self.learning_state = state
    return model_row

# Detect if there is an intersection
def intersection_detected(self, env):
    # C Callout
    dl.intersection_detected.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.intersection_detected.restype = c_bool
    is_intersection = dl.intersection_detected(env.c_info_struct, self.index)

    first_time = False
    if is_intersection and self.intersection_arrival == -1:
        self.intersection_arrival = self.step_count
        first_time = True

    # Return 
    return (is_intersection and first_time)

# Check if approaching an intersection
def approaching_intersection(self, env):
    # C Callout
    dl.approaching_intersection.argtypes = [POINTER(EnvironmentInfo), c_int]
    dl.approaching_intersection.restype = c_bool
    return dl.approaching_intersection(env.c_info_struct, self.index)

# Get the stopping points (~3/4 through the tile)
def get_stop_pos(self, env):
    # Get state information
    tile_x, tile_z = env.get_grid_coords(self.cur_pos) 
    tile_size = env.road_tile_size
    direction = self.direction

    # Adjust stop point based on speed
    # Treat agents above .30 as the same. Its just how it goes.
    speed = self.speed

    dl.get_stop_pos_x.argtypes = [c_int, c_int, c_float, c_int, c_float]
    dl.get_stop_pos_x.restype = c_float
    stop_pos_x = dl.get_stop_pos_x(int(tile_x), int(tile_z), float(tile_size), get_dl_direction(direction), float(speed))
    stop_x = round(float(stop_pos_x), 3)
    

    dl.get_stop_pos_z.argtypes = [c_int, c_int, c_float, c_int, c_float]
    dl.get_stop_pos_z.restype = c_float
    stop_pos_z = dl.get_stop_pos_z(int(tile_x), int(tile_z), float(tile_size), get_dl_direction(direction), float(speed))
    stop_z = round(float(stop_pos_z), 3)

    return stop_x, stop_z