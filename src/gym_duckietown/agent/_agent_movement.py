from .. import logger
from ..dl_utils import *
import numpy as np
import math
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
            curve_point, _ = env.closest_curve_point(follow_point, self.cur_angle, index=self.curve)
        else:
            curve_point, _ = env.closest_curve_point(follow_point, self.cur_angle, index=None)
        # If we have a valid point on the curve, stop
        if curve_point is not None:
            break

        iterations += 1
        lookup_distance *= 0.5

    # Compute a normalized vector to the curve point
    point_vec = curve_point - self.cur_pos
    point_vec /= np.linalg.norm(point_vec)
    dot = np.dot(get_right_vec(self.cur_angle), point_vec)
    #print(dot)

    # General Case
    steering = (forward_step*10) * -dot

    if self.states['in_intersection'] or self.states['at_intersection_entry']:
        if self.turn_choice == 'Right':
            forward_step = .20
            steering = (forward_step * 30) * -dot
        if self.turn_choice == 'Left':
            forward_step = .33
            steering = (forward_step * 13) * -dot
    else:
        if abs(dot) > 0.10:
            # Increase steering and slow us down
            steering = (forward_step*13) * -dot
            #print(f"Slowing down {forward_step}")
            forward_step = 3 * (forward_step / 4)

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