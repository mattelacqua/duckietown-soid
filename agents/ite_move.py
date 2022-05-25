import random
import numpy as np
import math
"""
Contains functions for moving agent in ite world scenarios.
"""

# Stop the vehicle
def stop_vehicle(wheel_distance, min_rad, forward_step, turn_step, action, env, args):
    # Get state information
    info = env.get_agent_info()
    curr_speed = info['Simulator']['robot_speed']

    # While still moving Slow down
    while curr_speed > 0.0009:
        action = np.array([0.0, 0.0])
        action = limit_rad_curvature(wheel_distance, min_rad, forward_step, turn_step, action, env, args)
        obs, reward, done, info = env.step(action)
        print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))
        render_step(done, env, args)

        # Check new speed
        info = env.get_agent_info()
        curr_speed = info['Simulator']['robot_speed']


# Take a right turn
def right_turn(wheel_distance, min_rad, forward_step, turn_step, action, env, args):
    # Get state information
    info = env.get_agent_info()
    curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
    if curr_angle < 0:
        curr_angle = abs(curr_angle) + 180
    direction = get_direction(env, args)

    # Made up the values for loop guard and turn step... May change on direction
    angle_limit = 0
    if direction == 'N':
        angle_limit = 27 
    elif direction == 'E':
        angle_limit = 245 
    elif direction == 'S':
        angle_limit = 335 
    elif direction == 'W':
        angle_limit = 115 

    if (direction == 'N' or direction == 'W'):
        while curr_angle > angle_limit:
            action = np.array([0.0, 0.0])
            action += np.array([forward_step, 0.0])
            action -= np.array([0.0, 3])
            obs, reward, done, info = env.step(action)
            print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))
            render_step(done, env, args)

            # Check new angle
            info = env.get_agent_info()
            curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
            if curr_angle < 0:
                curr_angle = abs(curr_angle) + 180
    else:
        while curr_angle < angle_limit:
            action = np.array([0.0, 0.0])
            action += np.array([forward_step, 0.0])
            action -= np.array([0.0, 3])
            obs, reward, done, info = env.step(action)
            print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))
            render_step(done, env, args)

            # Check new angle
            info = env.get_agent_info()
            curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
            if curr_angle < 0:
                curr_angle = abs(curr_angle) + 180


# Take a left turn
def left_turn(wheel_distance, min_rad, forward_step, turn_step, action, env, args):
    # Get state information
    info = env.get_agent_info()
    curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
    if curr_angle < 0:
        curr_angle = abs(curr_angle) + 180
    direction = get_direction(env, args)

    # Made up the values for loop guard and turn step... May change on direction
    angle_limit = 0
    if direction == 'N':
        angle_limit = 165 
    elif direction == 'E':
        angle_limit = 80
    elif direction == 'S':
        angle_limit = 192 
    elif direction == 'W':
        angle_limit = 280 

    if (direction == 'N' or direction == 'E'):
        while curr_angle < angle_limit:
            action = np.array([0.0, 0.0])
            action += np.array([forward_step, 0.0])
            action += np.array([0.0, 1.4])
            obs, reward, done, info = env.step(action)
            print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))
            render_step(done, env, args)

            # Check new angle
            info = env.get_agent_info()
            curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
            if curr_angle < 0:
                curr_angle = abs(curr_angle) + 180
    else:
        while curr_angle > angle_limit or curr_angle == 180:
            action = np.array([0.0, 0.0])
            action += np.array([forward_step, 0.0])
            action += np.array([0.0, 1.4])
            obs, reward, done, info = env.step(action)
            print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))
            render_step(done, env, args)

            # Check new angle
            info = env.get_agent_info()
            curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
            if curr_angle < 0:
                curr_angle = abs(curr_angle) + 180



# Move forward through tile
def move_through_tile(wheel_distance, min_rad, forward_step, turn_step, action, env, args):
    # Get current tile
    info = env.get_agent_info()
    original_tile = info['Simulator']['tile_coords']
    current_tile = original_tile

    # While still on same tile, move forward the rest of the way
    while current_tile == original_tile:
        action = np.array([0.0, 0.0])
        action += np.array([0.44, 0.0])
        action = limit_rad_curvature(wheel_distance, min_rad, forward_step, turn_step, action, env, args)
        obs, reward, done, info = env.step(action)
        print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))
        render_step(done, env, args)

        # Check tile
        info = env.get_agent_info()
        current_tile = info['Simulator']['tile_coords']

# Handle an intersection by turning right (default)
def handle_intersection(wheel_distance, min_rad, forward_step, turn_step, action, env, args, choice):
    info = env.get_agent_info()
    # Stop
    stop_vehicle(wheel_distance, min_rad, forward_step, turn_step, action, env, args)

    # Choose a random option
    choices = ['Right', 'Left', 'Straight'] 
    if choice == None:
        choice = random.choice(choices)

    # Move based on choice
    if choice == 'Right':
        right_turn(wheel_distance, min_rad, forward_step, turn_step, action, env, args)
    elif choice == 'Left':
        left_turn(wheel_distance, min_rad, forward_step, turn_step, action, env, args)
    elif choice == 'Straight':
        move_through_tile(wheel_distance, min_rad, forward_step, turn_step, action, env, args)

    # Move Straight till next tile
    current_tile = info['Simulator']['tile_coords']
    if intersection_tile(current_tile[0], current_tile[1], env):
        move_through_tile(wheel_distance, min_rad, forward_step, turn_step, action, env, args)

# Detect if there is an intersection
def intersection_detected(wheel_distance, min_rad, forward_step, turn_step, action, env, args):
    # Get relevant state information
    info = env.get_agent_info()
    tile_x, tile_z = info['Simulator']['tile_coords']
    tile_size = env.road_tile_size
    direction = get_direction(env, args)
    stop_x, stop_z = get_stop_check(env, args)
    curr_x = info['Simulator']['cur_pos'][0] * tile_size
    curr_z = info['Simulator']['cur_pos'][2] * tile_size

    # Based on direction check intersection
    if direction == 'N' and curr_z < stop_z and approaching_intersection(env, args):
        return True
    elif direction == 'W' and curr_x < stop_x and approaching_intersection(env, args):
        return True
    elif direction == 'S' and curr_z > stop_z and approaching_intersection(env, args):
        return True
    elif direction == 'E' and curr_x > stop_x and approaching_intersection(env, args):
        return True
    else:
        return False

# Get current direction
def get_direction(env, args):
    # Get state information
    info = env.get_agent_info()
    curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
    if curr_angle < 0:
        curr_angle = abs(curr_angle) + 180

    # Based on the current angle of the agent return a direction it is moving
    if curr_angle > 45 and curr_angle <= 135:
        return 'N'
    elif curr_angle > 225  and curr_angle <= 315:
        return 'S'
    elif (curr_angle > 180  and curr_angle <= 225) or (curr_angle >= 0 and curr_angle <= 45):
        return 'E'
    else:
        return 'W'


# Get the stopping points (~3/4 through the tile)
def get_stop_check(env, args):
    # Get state information
    info = env.get_agent_info()
    tile_x, tile_z = info['Simulator']['tile_coords']
    tile_size = env.road_tile_size
    curr_x = info['Simulator']['cur_pos'][0] * tile_size
    curr_z = info['Simulator']['cur_pos'][2] * tile_size
    direction = get_direction(env, args)

    # get the 2/3ish length of tile to go through
    if direction == 'N':
        stop_x = (tile_x * tile_size) - (tile_size/2)
        stop_z = (tile_z * tile_size) - (tile_size/1.5)
    elif direction == 'W': 
        stop_x = (tile_x * tile_size) - (tile_size/1.5)
        stop_z = (tile_z * tile_size) - (tile_size/2)
    elif direction == 'S': 
        stop_x = (tile_x * tile_size) + (tile_size/2)
        stop_z = (tile_z * tile_size) + (tile_size/2.5)
    elif direction == 'E': 
        stop_x = (tile_x * tile_size) + (tile_size/2.45)
        stop_z = (tile_z * tile_size) + (tile_size/2)

    return stop_x, stop_z

# Check if approaching an intersection
def approaching_intersection(env, args):
    # Get state information
    info = env.get_agent_info()
    tile_x, tile_z = info['Simulator']['tile_coords']
    direction = get_direction(env, args)

    # Based on direction, check if the next tile is an intersection
    if direction == 'N' and intersection_tile(tile_x, tile_z-1, env):
        return True
    elif direction == 'W' and intersection_tile(tile_x-1, tile_z, env):
        return True
    elif direction == 'S' and intersection_tile(tile_x, tile_z+1, env):
        return True
    elif direction == 'E' and intersection_tile(tile_x+1, tile_z, env):
        return True
    else:
        return False

# Check if a tile is an intersection tile
def intersection_tile(tile_x, tile_z, env):
    if tile_x >= 0 and tile_z >= 0 and tile_x < env.grid_width and tile_z < env.grid_height:
        tile_kind = env._get_tile(tile_x, tile_z)['kind']
        if tile_kind == '4way':
            return True
        else:
            return False
    else:
        return False

# function for limiting radius of curvature
def limit_rad_curvature(wheel_distance, min_rad, forward_step, turn_step, action, env, args):
    v1 = action[0]
    v2 = action[1]
    # Limit radius of curvature
    if v1 == 0 or abs(v2 / v1) > (min_rad + wheel_distance / 2.0) / (min_rad - wheel_distance / 2.0):
        # adjust velocities evenly such that condition is fulfilled
        delta_v = (v2 - v1) / 2 - wheel_distance / (4 * min_rad) * (v1 + v2)
        v1 += delta_v
        v2 -= delta_v
    return v1, v2


# Render if possible, otherwise end if invalid
def render_step(done, env, args):
    # if hit obstacle, return and stop
    # otherwise, keep going and render in the proper cam mode
    if done:
        env.reset()
        return False
    else:
        env.render(args.cam_mode)
        return True
