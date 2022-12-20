from .. import logger
from ..dl_utils import *
import numpy as np
import math
import time
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


# Move along path
def move_forward(self, env, speed_limit=1.0, intersection=False):
    # Set the speed
    forward_step = self.forward_step
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

    # Get forward step
    forward_step = self.forward_step
    control_gain = 2
    speed_proportional_gain = 3.0

    #print(self.turn_choice)

    if forward_step == 0.0:
        return actions.append(([forward_step, 0], Action.STOP))

    # Find the curve point closest to the agent (this will change if we are at an intersection), and the tangent at that point
    if self.states['at_intersection_entry'] or self.states['in_intersection']:
        closest_point, closest_tangent = env.closest_curve_point(self.cur_pos, self.cur_angle, index=self.curve)
        #print(self.turn_choice)
        #print("SET THE POINT HERE")
    else:
        closest_point, closest_tangent = env.closest_curve_point(self.cur_pos, self.cur_angle, index=None)
    if closest_point is None or closest_tangent is None:
        msg = f"Cannot find closest point/tangent from {self.cur_pos}, {self.cur_angle} "
        # Do a default move forward
        #print("DEF CASE")
        actions.append(([forward_step, 0], Action.FORWARD_STEP))
        return actions


    iterations = 0
    lookup_distance = self.follow_dist
    curve_point = None
    while iterations < self.max_iterations:
        # Project a point ahead along the curve tangent,
        # then find the closest point to to that
        follow_point = closest_point + closest_tangent * lookup_distance
        if self.states['at_intersection_entry'] or self.states['in_intersection']:
            curve_point, curve_tangent = env.closest_curve_point(follow_point, self.cur_angle, index=self.curve)
        else:
            curve_point, curve_tangent = env.closest_curve_point(follow_point, self.cur_angle, index=None)
        # If we have a valid point on the curve, stop
        if curve_point is not None:
            break

        iterations += 1
        lookup_distance *= 0.5

    point_vec = curve_point - self.cur_pos
    point_vec /= np.linalg.norm(point_vec)
    dot = np.dot(get_right_vec(self.cur_angle), point_vec)
    # Compute a normalized vector to the curve point
    """
    point_vec = curve_point - self.cur_pos
    point_vec /= np.linalg.norm(point_vec)
    point_vec_error = np.dot(get_right_vec(self.cur_angle), point_vec)
    cross_track_error = np.arctan2(control_gain * point_vec_error, self.speed)

    # Computer normalized angle error:
    direction_vec = get_dir_vec(self.cur_angle)
    direction_vec_error = np.dot(direction_vec, curve_tangent)
    direction_vec_error = np.clip(direction_vec_error, -1.0, +1.0)
    
    total_error = direction_vec_error + cross_track_error
    print(total_error)
    """

    if self.states['at_intersection_entry'] or self.states['in_intersection']:
        print('this index')
        lane_pos = env.get_lane_pos2(self.cur_pos, self.cur_angle, index=self.curve)
    else:
        print("HEREERE")
        lane_pos = env.get_lane_pos2(self.cur_pos, self.cur_angle)
   

    # General Case
    """
    steering = (self.forward_step * 10) * -dot
    ready_to_accelerate = False
    if self.direction == 'N' and 88 < self.get_curr_angle(env) < 92:
        ready_to_accelerate = 'N'
    elif self.direction == 'S' and 268 < self.get_curr_angle(env) < 272:
        ready_to_accelerate = 'S'
    elif self.direction == 'E' and (0 <= self.get_curr_angle(env) < 2 or 358 < self.get_curr_angle(env) <= 360):
        ready_to_accelerate = 'E'
    elif self.direction == 'W' and 178 < self.get_curr_angle(env) < 182:
        ready_to_accelerate = 'W'
    """

    if self.states['in_intersection'] or self.states['at_intersection_entry']:# or not ready_to_accelerate:
        #if not ready_to_accelerate:
        #    print(f"Not ready to accel: {ready_to_accelerate}")
        if self.turn_choice == 'Right':
            forward_step = .35
            control_gain = 20

        if self.turn_choice == 'Left':
            forward_step = .60
            control_gain = 20
            #steering = (forward_step * 13) * -dot

    cross_track_error = lane_pos.dist
    direction_error = lane_pos.angle_rad
    total_error = cross_track_error + direction_error
    print(f"CTE: {cross_track_error} DR: {direction_error} TE: {total_error}")
    steering = total_error * control_gain
    forward_step = (forward_step - self.speed) - cross_track_error * speed_proportional_gain
    #else:
    # Limit radius of curvature
    wheel_distance = 0.102
    min_rad = 0.8
    speed = self.speed

    #if forward_step == 0 or abs(speed / forward_step) > (min_rad + wheel_distance / 2.0) / (min_rad - wheel_distance / 2.0):
    #    # adjust velocities evenly such that condition is fulfilled
    #    delta_v = (forward_step - speed) / 2 - wheel_distance / (4 * min_rad) * (forward_step + steering)
    #    forward_step += delta_v
    #k    steering -= delta_v
 
 
    if intersection:
        actions.append(([forward_step, steering], Action.INTERSECTION_FORWARD))
    else:
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