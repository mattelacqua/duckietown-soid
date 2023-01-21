from ..agents import dl
from ..dl_utils import *
#--------------------------
# Intersections 
# Code for handling intersection behavior
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

    # Stop before entering intersection
    action_seq.extend(self.stop_vehicle(env))

    action_seq.extend(self.move_forward(env, speed_limit=speed_limit, intersection=True))

    return action_seq

# Get the stopping points (~3/4 through the tile)
def get_stop_pos(self, env):
    # Get state information
    tile_x, tile_z = env.get_grid_coords(self.cur_pos) 
    tile_size = env.road_tile_size
    direction = self.direction

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
