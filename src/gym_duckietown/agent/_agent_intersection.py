from ..agents import dl
from ..dl_utils import *
#--------------------------
# Intersections 
# Code for handling intersection behavior
#--------------------------

# Handle an intersection
def handle_intersection(self, env, speed_limit=1.0,  stop_point=30, learning=False):
    # Set its intersection arrival time
    # Initialize action sequence
    action_seq = []

    # Stop before entering intersection
    action_seq.extend(self.stop_vehicle(env))

    action_seq.extend(self.move_forward(env, speed_limit=speed_limit, intersection=True))

    return action_seq


