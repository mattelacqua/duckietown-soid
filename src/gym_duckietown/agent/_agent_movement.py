from .. import logger
from ..dl_utils import *
import numpy as np
import math
import time
#--------------------------
# Movement
#--------------------------

# Stop the vehicle
def stop_vehicle(self, env, stop_point: int=30):

    if env.verbose:
        logger.info(self.agent_id + ": Stopping")
    stop_iterations = 0

    # Initialize action sequence
    action_seq = []

    # While still moving Slow down
    while stop_iterations < stop_point:
        action = np.array([0.0, 0.0])
        action_seq.append((action, Action.INTERSECTION_STOP))
        self.signal_for_turn(self.signal_choice)
        stop_iterations += 1

    return action_seq


# Move along path
def move_forward(self, env, speed_limit=1.0, intersection=False):

    # Set the speed
    forward_step = self.forward_step
    
    # If we are stopped we do nothing. 
    if forward_step == 0.0:
        return []

    # Get state information
    curr_speed = self.speed
    if env.verbose:
        logger.info(self.agent_id + ": Moving Forwards at speed " + str(curr_speed))

    # Initialize action sequence
    action_seq = []

    # While still moving Slow down
    if curr_speed > speed_limit:
        action = np.array([0.0, 0.0])
        action_seq.append((action, Action.SLOW_DOWN))
    else:
        action_seq.extend(self.straighten_out(env, intersection=intersection))

    # Turn off all lights because moving straight (either initially or after turning)
    self.turn_off_light("front_right")
    self.turn_off_light("back_right")
    self.turn_off_light("front_left")
    self.turn_off_light("back_left")

    return action_seq

# Straighten out and follow curve
def straighten_out(self, env, intersection=False):
    from ..simulator import get_right_vec, get_dir_vec
    actions = []


    # If we don't want to move at all
    forward_step = self.forward_step
    if forward_step == 0.0:
        return actions.append(([forward_step, 0], Action.STOP))

    # Find the curve point closest to the agent (this will change if we are at an intersection), and the tangent at that point
    if self.states['at_intersection_entry'] or self.states['in_intersection']:
        closest_point, closest_tangent = env.closest_curve_point(self.cur_pos, self.cur_angle, index=self.curve, intersection=True)
    else:
        closest_point, closest_tangent = env.closest_curve_point(self.cur_pos, self.cur_angle, index=self.get_curve(env, straight=True))
    if closest_point is None or closest_tangent is None:
        msg = f"Cannot find closest point/tangent from {self.cur_pos}, {self.cur_angle} "
        actions.append(([forward_step, 0], Action.FORWARD_STEP))
        return actions

    # Find a projection point
    iterations = 0
    lookup_distance = self.follow_dist
    curve_point = None
    while iterations < self.max_iterations:
        # Project a point ahead along the curve tangent,
        # then find the closest point to to that
        follow_point = closest_point + closest_tangent * lookup_distance
        if self.states['at_intersection_entry'] or self.states['in_intersection']:
            curve_point, curve_tangent = env.closest_curve_point(follow_point, self.cur_angle, index=self.curve, intersection=True)
        else:
            curve_point, curve_tangent = env.closest_curve_point(follow_point, self.cur_angle, index=self.get_curve(env, straight=True))
        # If we have a valid point on the curve, stop
        if curve_point is not None:
            break

        iterations += 1
        lookup_distance *= 0.5

    # Get lane position information to calculate error
    if self.states['at_intersection_entry'] or self.states['in_intersection']:
        lane_pos = env.get_lane_pos2(self.cur_pos, self.cur_angle, index=self.curve, intersection=True)
    else:
        lane_pos = env.get_lane_pos2(self.cur_pos, self.cur_angle, index=self.get_curve(env, straight=True))
    
    # Get forward step
    cross_track_gain = 15.0
    direction_gain = 10.0
    speed_gain = 1

    # Steering adjustments
    if self.states['in_intersection'] or self.states['at_intersection_entry']:
        if self.turn_choice == 'Right':
            forward_step *= 0.7
            cross_track_gain *= 1.2
            direction_gain *= 1.2
            speed_gain *= 0.5

        if self.turn_choice == 'Left':
            forward_step *= 0.7

    # Make cross track error and direction error dependent on our coefficients
    cross_track_error = lane_pos.dist 
    direction_error = lane_pos.angle_rad
    total_error = (cross_track_error * cross_track_gain) + (direction_error * direction_gain)
    speed_penalty = abs(cross_track_error + direction_error)
    #print(f'CTE {cross_track_error} DE {direction_error} TE {total_error} SF {speed_penalty}')
    steering = total_error 

    #forward_step = (forward_step - self.speed) - total_error
    forward_step = forward_step - (speed_gain * speed_penalty)
 
    # If we are in an intersection
    if intersection:
        actions.append(([forward_step, steering], Action.INTERSECTION_FORWARD))
    else:
        actions.append(([forward_step, steering], Action.FORWARD_STEP))

    return actions