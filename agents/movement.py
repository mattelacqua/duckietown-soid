import random
import numpy as np
import math
"""
Contains functions for moving agent in ite world scenarios.
"""

# Stop the vehicle
def stop_vehicle(env):
    print("Stopping the Vehicle")
    # Get state information
    curr_speed = get_curr_speed(env)

    # While still moving Slow down
    while curr_speed > 0.0009:
        action = np.array([0.0, 0.0])
        assert render_step(env, action), "Failed Stopping Vehicle"

        # Check new speed
        curr_speed = get_curr_speed(env)

# Move Forwards at whatever angle we are at, not going faster than 30 mps
def move_forward(env, forward_step, speed_limit):
    # Get state information
    curr_speed = get_curr_speed(env)
    print("Moving Forwards at speed " + str(curr_speed))

    # While still moving Slow down
    if curr_speed > speed_limit:
        action = np.array([0.0, 0.0])
        assert render_step(env, action), "Failed Moving Forward Over Speed Limit"
    else:
        action = np.array([0.0, 0.0])
        action += np.array([forward_step, 0.0])
        assert render_step(env, action), "Failed Moving Forward Under Speed Limit"

# Straighten out TODO
def straighten_out(env):
    print("Straightening out")

# Take a right turn
def right_turn(env, forward_step):
    print("Taking a right turn")
    # Get state information
    curr_angle = get_curr_angle(env)
    turn_count = 0
    direction = get_direction(env)

    # Turn this amount 
    while turn_count < 26:          # Arbitrary turn count that works for speed limit?
        action = np.array([0.0, 0.0])
        action -= np.array([0.0, 4])
        action += np.array([forward_step, 0.0])
        assert render_step(env, action), "Failed turning right"
        turn_count += 1

    # Straighten Out
    straighten_out(env)

# Take a left turn
def left_turn(env, forward_step):
    print("Taking a right turn")
    # Get state information
    curr_angle = get_curr_angle(env)
    turn_count = 0
    direction = get_direction(env)

    # Turn this amount 
    while turn_count < 75:          # Arbitrary turn count that works for speed limit?
        action = np.array([0.0, 0.0])
        action += np.array([0.0, 1.5])
        action += np.array([forward_step, 0.0])
        assert render_step(env, action), "Failed turning left"
        turn_count += 1   

    # Turn this amount 
    straighten_out(env)


# Move forward through tile
def move_through_tile(env, forward_step, speed_limit):
    # Get current tile
    original_tile = get_current_tile(env)
    current_tile = original_tile

    # While still on same tile, move forward the rest of the way
    while current_tile == original_tile:
        # Move Straight
        move_forward(env, forward_step, speed_limit)

        # Check tile
        current_tile = get_current_tile(env) 

# Handle an intersection by turning right (default)
def handle_intersection(env, forward_step, speed_limit, choice):
    info = env.get_agent_info()

    # Stop
    stop_vehicle(env)

    # Choose a random option if one not given
    choices = ['Right', 'Left', 'Straight'] 
    if choice == None:
        choice = random.choice(choices)

    # Move based on choice
    if choice == 'Right':
        right_turn(env, forward_step)
    elif choice == 'Left':
        left_turn(env, forward_step)
    elif choice == 'Straight':
        move_forward(env, forward_step, speed_limit)

# Detect if there is an intersection
def intersection_detected(env):
    # Get relevant state information
    curr_x, curr_z = get_curr_pos(env)
    stop_x, stop_z = get_stop_pos(env)
    direction = get_direction(env)

    # Based on direction check intersection
    if direction == 'N' and curr_z < stop_z and approaching_intersection(env):
        return True
    elif direction == 'W' and curr_x < stop_x and approaching_intersection(env):
        return True
    elif direction == 'S' and curr_z > stop_z and approaching_intersection(env):
        return True
    elif direction == 'E' and curr_x > stop_x and approaching_intersection(env):
        return True
    else:
        return False

# Get the stopping points (~3/4 through the tile)
def get_stop_pos(env):
    # Get state information
    tile_x, tile_z = get_curr_tile(env)['coords']
    tile_size = env.road_tile_size
    curr_x, curr_z = get_curr_pos(env)
    direction = get_direction(env)

    # get the 2/3ish length of tile to go through
    if direction == 'N':
        stop_x = (tile_x * tile_size) - (tile_size/2)
        stop_z = ((tile_z + 1) * tile_size) - (tile_size/4) * 3           # split tile up into 3, subtract 2 from bottom since we are going up
    elif direction == 'W': 
        stop_x = ((tile_x + 1) * tile_size) - (tile_size/4) * 3         # split tile up into 3, subtract 2 from bottom since we are going up
        stop_z = (tile_z * tile_size) - (tile_size/2)
    elif direction == 'S': 
        stop_x = (tile_x * tile_size) + (tile_size/2) 
        stop_z = (tile_z * tile_size) + (tile_size/4) * 3
    elif direction == 'E': 
        stop_x = (tile_x * tile_size) + (tile_size/4) * 3 
        stop_z = (tile_z * tile_size) + (tile_size/2)

    return stop_x, stop_z

# Check if approaching an intersection
def approaching_intersection(env):
    # Get state information
    tile_x, tile_z = get_curr_tile(env)['coords']
    direction = get_direction(env)

    # Based on direction, check if the next tile is an intersection
    if direction == 'N' and intersection_tile(env, tile_x, tile_z-1):
        return True
    elif direction == 'W' and intersection_tile(env, tile_x-1, tile_z):
        return True
    elif direction == 'S' and intersection_tile(env, tile_x, tile_z+1):
        return True
    elif direction == 'E' and intersection_tile(env, tile_x+1, tile_z):
        return True
    else:
        return False

# Check if a tile is an intersection tile
def intersection_tile(env, tile_x, tile_z):
    if tile_x >= 0 and tile_z >= 0 and tile_x < env.grid_width and tile_z < env.grid_height:
        tile_kind = get_tile(env, tile_x, tile_z)['kind']
        if tile_kind == '4way':
            return True
        else:
            return False
    else:
        return False

# Get current direction
def get_direction(env):
    # Get state information
    curr_angle = get_curr_angle(env)

    # Based on the current angle of the agent return a direction it is moving
    if curr_angle > 45 and curr_angle <= 135:
        return 'N'
    elif curr_angle > 225  and curr_angle <= 315:
        return 'S'
    elif curr_angle > 135   and curr_angle <= 225:
        return 'W'
    else:
        return 'E'

# Get current angle degrees
def get_curr_angle(env):
    info = env.get_agent_info()
    curr_angle = round(math.degrees(info['Simulator']['cur_angle']))
    if curr_angle < 0:
        curr_angle = 360 - abs(curr_angle)

    return curr_angle

# Get Current Speed
def get_curr_speed(env):
    info = env.get_agent_info()
    return info['Simulator']['robot_speed']

# Get current tile info
def get_curr_tile(env):
    info = env.get_agent_info()
    tile_x, tile_z = info['Simulator']['tile_coords']
    return env._get_tile(tile_x, tile_z)

# Get tile info
def get_tile(env, tile_x, tile_z):
    return env._get_tile(tile_x, tile_z)

# Get current position
def get_curr_pos(env):
    info = env.get_agent_info()
    tile_size = env.road_tile_size
    current_tile = get_curr_tile(env)['coords']
    curr_x = info['Simulator']['cur_pos'][0]
    curr_z = info['Simulator']['cur_pos'][2]
    return curr_x, curr_z

# Render the step and call the inner return
def render_step(env, action):
    obs, reward, done, info = env.step(action)
    print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))
    return render_step_inner(env, done)


# Render if possible, otherwise end if invalid
def render_step_inner(env, done):
    # if hit obstacle, return and stop
    # otherwise, keep going and render in the proper cam mode
    if done:
        print("Failed")
        env.reset()
        return False
    else:
        env.render(env.cam_mode)
        return True
