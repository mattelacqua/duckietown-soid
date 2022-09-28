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


# Move Forwards at whatever angle we are at, not going faster than 30 mps
def move_forward(self, env, speed_limit=1.0):
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
        action_seq.extend(self.straighten_out(env))

    # Turn off all lights because moving straight (either initially or after turning)
    self.turn_off_light("front_right")
    self.turn_off_light("back_right")
    self.turn_off_light("front_left")
    self.turn_off_light("back_left")

    return action_seq

# Straighten out and follow curve
def straighten_out(self, env):
    from ..simulator import get_right_vec
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
        # Do a default move forward
        actions.append(([forward_step, 0], Action.FORWARD_STEP))
        return actions


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
    #print(f"Executing a right turn for {self.agent_id}, turn steps is {turn_stop}")
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