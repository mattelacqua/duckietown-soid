from ..agents import dl, so_file
from ..dl_utils import *
from ._agent_utils import intersection_tile
import time
#--------------------------
# Intersections 
#--------------------------

# Handle an intersection
def handle_intersection(self, env, speed_limit=1.0,  stop_point=30, learning=False):
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
    #print("CALLING INTERSECTION ACTION")
    intersection_action_addr = dl.intersection_action(turn_choice, signal_choice, self.intersection_arrival if self.intersection_arrival else env.max_steps, env_agent_array_struct)
    intersection_action = IntersectionAction.from_address(intersection_action_addr)
    turn_choice = TurnChoice(intersection_action.turn_choice)
    signal_choice = TurnChoice(intersection_action.signal_choice)
    action = Action(intersection_action.action)
    wait_step = intersection_action.wait_step

    # Every Agent Stops
    # Cushion slow down to stop at intersectoin
    # For learning we want our agent to just stop

    # Stop before entering intersection if not the learning agent
    if not learning:
        action_seq.extend(self.stop_vehicle(env, signal_choice, forward_step=forward_step))
    elif learning and self.agent_id != "agent0":
        action_seq.extend(self.stop_vehicle(env, signal_choice, forward_step=forward_step))

    if action == Action.INTERSECTION_RIGHT:
        if self.agent_id == "agent0":
            print(f"{self.agent_id} is taking a right turn.")
        action_seq.extend(self.right_turn(env, forward_step=forward_step))
    elif action == Action.INTERSECTION_LEFT:
        #print(f"{self.agent_id} is taking a left turn.")
        if self.agent_id == "agent0":
            print(f"{self.agent_id} is taking a left turn.")
        action_seq.extend(self.left_turn(env, forward_step=forward_step))
    elif action == Action.INTERSECTION_FORWARD:
        #print(f"{self.agent_id} is going straight.")
        if self.agent_id == "agent0":
            print(f"{self.agent_id} is taking a straight.")
        forward_steps = 0
        while forward_steps < 30:
            action_seq.extend(self.move_forward(env, speed_limit=speed_limit, intersection=True))
            forward_steps += 1 

    return action_seq

# Detect if there is an intersection
def intersection_detected(self, env):
    # Get relevant state information
    curr_x, curr_z = self.cur_pos[0], self.cur_pos[2]
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

    first_time = False
    if is_intersection and not self.intersection_arrival:
        self.intersection_arrival = self.step_count
        first_time = True
        #print("\n\nHERE\n\n")
    

    # Return 
    return (is_intersection and first_time)

# Check if approaching an intersection
def approaching_intersection(self, env, include_tile: bool=False):
    # Get state information
    if self.in_bounds(env):
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
    else:
        if include_tile:
            return False, None
        else:
            return False

# Check if approaching an intersection
def left_intersection(self, env, include_tile: bool=False):
    # Get state information
    tile_x, tile_z = list(env.get_grid_coords(self.cur_pos))
    prev_tile_x, prev_tile_z = list(env.get_grid_coords(self.prev_pos))

    if intersection_tile(env, prev_tile_x, prev_tile_z) and not intersection_tile(env, tile_x, tile_z):
        return True        
    else:
        return False


# Get the stopping points (~3/4 through the tile)
def get_stop_pos(self, env):
    # Get state information
    tile_x, tile_z = env.get_grid_coords(self.cur_pos) 
    tile_size = env.road_tile_size
    curr_x, curr_z = self.cur_pos[0], self.cur_pos[2]
    direction = self.get_direction(env)
    # Adjust stop point based on speed

    # Treat agents above .30 as the same. Its just how it goes.
    speed = self.speed

    if speed > .35:
        speed = .30
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