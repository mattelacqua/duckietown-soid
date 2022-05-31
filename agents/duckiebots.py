import random
import numpy as np
import math
import movement as move
# Get object info
def get_objects(env):
    objects = env.objects
    print("Objects:")
    for obj in objects:
        print(vars(obj))
    exit()

# Update each duckiebot position
def update_duckiebots(env):
    delta_time = env.delta_time
    db_action_pairs = get_agent_duckiebot_moves(env)
    for (duckiebot, action) in db_action_pairs:
        duckiebot._update_pos(action, delta_time)


# Get next move for each duckiebot, return list of actions
def get_agent_duckiebot_moves(env):
    duckiebots = get_agent_duckiebots(env)
    actions = []
    for duckiebot in duckiebots:
        actions.append(get_agent_duckiebot_action(env, duckiebot))
    return list(zip(duckiebots, actions))

# Get next action for a single duckiebot
def get_agent_duckiebot_action(env, duckiebot):
    print("Pass")
    return [0, 0]


# Get all controllable duckiebots from the objects
def get_agent_duckiebots(env):
    objects = env.objects
    duckiebots = [] 
    for obj in objects:
        info = obj.get_object_info()
        if info['kind'] == 'duckiebot' and info['agent']:
            duckiebots.append(obj)
    return duckiebots

