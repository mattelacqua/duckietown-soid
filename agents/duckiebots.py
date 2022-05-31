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

# Get next move for each duckiebot, return list of actions
def update_duckiebots(env):
    duckiebots = get_agent_duckiebots(env)
    actions = []
    for duckiebot in duckiebots:
        next_action = get_next_duckiebot_action(env, duckiebot)
        actions.append(next_action)
    return list(zip(duckiebots, actions))

# Get the next action and perform it
def get_next_duckiebot_action(env, duckiebot):
    # Check if action to take
    actions = duckiebot.get_actions()
    if actions != None:
        return actions[0]
    else:
        duckiebot_step(env, duckiebot)
        return get_next_duckiebot_action(env, duckiebot)


# General step for duckiebot
def duckiebot_step(env, duckiebot): 
    if move.intersection_detected(env, duckiebot=duckiebot):
        move.handle_intersection(env, duckiebot=duckiebot, forward_step=0.1)
    else:
        move.move_forward(env, duckiebot=duckiebot, forward_step=0.1)


# Get all controllable duckiebots from the objects
def get_agent_duckiebots(env):
    objects = env.objects
    duckiebots = [] 
    for obj in objects:
        info = obj.get_object_info()
        if info['kind'] == 'duckiebot' and info['agent']:
            duckiebots.append(obj)
    return duckiebots

