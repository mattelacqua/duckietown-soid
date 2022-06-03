#!/usr/bin/env python
# manual

"""
This script uses the ite_move library to make a right turn through an intersection
"""
from PIL import Image
import argparse
import sys

import gym
import numpy as np
import pyglet
from pyglet.window import key

from gym_duckietown.envs import DuckietownEnv

# Includes all important moving functions for if then else agents
#import movement as move
import duckiebots as db 
import gym_duckietown.agents
import logging

# from experiments.utils import save_img

parser = argparse.ArgumentParser()
parser.add_argument("--env-name", default=None)
parser.add_argument("--map-name", default="udem1")
parser.add_argument("--distortion", default=False, action="store_true")
parser.add_argument("--camera_rand", default=False, action="store_true")
parser.add_argument("--draw-curve", action="store_true", help="draw the lane following curve")
parser.add_argument("--draw-bbox", action="store_true", help="draw collision detection bounding boxes")
parser.add_argument("--domain-rand", action="store_true", help="enable domain randomization")
parser.add_argument("--dynamics_rand", action="store_true", help="enable dynamics randomization")
parser.add_argument("--frame-skip", default=1, type=int, help="number of frames to skip")
parser.add_argument("--seed", default=1, type=int, help="seed")
parser.add_argument("--cam-mode", default="human", help="Camera modes: human, top_down, free_cam, rgb_array")
parser.add_argument("--safety-factor", default=1.0, type=float, help="Minimum distance before collision detection")
parser.add_argument("--num-agents", default=1.0, type=int, help="Number of Agents")
args = parser.parse_args()

if args.env_name and args.env_name.find("Duckietown") != -1:
    env = DuckietownEnv(
        seed=args.seed,
        map_name=args.map_name,
        cam_mode=args.cam_mode,
        safety_factor=args.safety_factor,
        num_agents=args.num_agents,
        draw_curve=args.draw_curve,
        draw_bbox=args.draw_bbox,
        domain_rand=args.domain_rand,
        frame_skip=args.frame_skip,
        distortion=args.distortion,
        camera_rand=args.camera_rand,
        dynamics_rand=args.dynamics_rand,
        full_transparency=True
    )
else:
    env = gym.make(args.env_name)

# Start up env
env.reset()
env.render(args.cam_mode)

# Global holders for each agents actions
agent0_actions = []
agent1_actions = []
agent2_actions = []
agent3_actions = []

def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    # Use global action lists
    global agent0_actions
    global agent1_actions
    global agent2_actions
    global agent3_actions

    # Get the agents
    agent0 = env.agents[0] 
    agent1 = env.agents[1] 
    agent2 = env.agents[2] 
    agent3 = env.agents[3] 

    # If we are not handling a sequence already, try for agent 0
    if not agent0_actions:
        if agent0.intersection_detected(env):
            agent0_actions.extend(agent0.handle_intersection(env, choice='Right'))
        else: 
            agent0_actions.extend(agent0.move_forward(env, forward_step=0.44))

    # If we are not handling a sequence already, try for agent 1
    if not agent1_actions:
        if agent1.intersection_detected(env):
            agent1_actions.extend(agent1.handle_intersection(env, choice='Right'))
        else: 
            agent1_actions.extend(agent1.move_forward(env, forward_step=0.44))

    # If we are not handling a sequence already, try for agent 2
    if not agent2_actions:
        if agent2.intersection_detected(env):
            agent2_actions.extend(agent2.handle_intersection(env, choice='Right'))
        else: 
            agent2_actions.extend(agent2.move_forward(env, forward_step=0.44))

    # If we are not handling a sequence already, try for agent 3
    if not agent3_actions:
        if agent3.intersection_detected(env):
            agent3_actions.extend(agent3.handle_intersection(env, choice='Right'))
        else: 
            agent3_actions.extend(agent3.move_forward(env, forward_step=0.44))

   
    # HERE WE CAN DO A CHECK TO SEE IF WE CHANGE THE SEQUENCES OR NOT BASED ON CURRENT STATE.
        #TODO:
    
    # Render each agent's next move
    agent0.render_step(env, agent0_actions.pop(0))
    agent1.render_step(env, agent1_actions.pop(0))
    agent2.render_step(env, agent2_actions.pop(0))
    agent3.render_step(env, agent3_actions.pop(0))
   
    # render the cam
    env.render(env.cam_mode)

# Enter main event loop
pyglet.clock.schedule_interval(update, 1.0 / env.unwrapped.frame_rate)
pyglet.app.run()

env.close()


    
