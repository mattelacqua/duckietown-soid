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

from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 0, 0, 255]}, resources_path='')


def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    # Get the agents
    agent0 = env.agents[0] 
    agent1 = env.agents[1] 
    agent2 = env.agents[2] 
    agent3 = env.agents[3] 

    speed0 = 0.2
    speed1 = 0.1
    speed2 = 0.8
    speed3 = 0.4
    turn = 'Left'

    # If we are not handling a sequence already, try for agent 0
    if not agent0.actions:
        if agent0.intersection_detected(env):
            print("HIT THIS CASE")
            agent0.add_actions(agent0.handle_intersection(env, choice=turn, forward_step=speed0))
        else: 
            agent0.add_actions(agent0.move_forward(env, forward_step=speed0))

    # If we are not handling a sequence already, try for agent 1
    if not agent1.actions:
        if agent1.intersection_detected(env):
            agent1.add_actions(agent1.handle_intersection(env, choice=turn, forward_step=speed1))
        else: 
            agent1.add_actions(agent1.move_forward(env, forward_step=speed1))

    # If we are not handling a sequence already, try for agent 1
    if not agent2.actions:
        if agent2.intersection_detected(env):
            agent2.add_actions(agent2.handle_intersection(env, choice=turn, forward_step=speed2))
        else: 
            agent2.add_actions(agent2.move_forward(env, forward_step=speed2))

     # If we are not handling a sequence already, try for agent 1
    if not agent3.actions:
        if agent3.intersection_detected(env):
            agent3.add_actions(agent3.handle_intersection(env, choice=turn, forward_step=speed3))
        else: 
            agent3.add_actions(agent3.move_forward(env, forward_step=speed3))
          
    # Render each agent's next move
    if agent0.actions:
        agent0.render_step(env, agent0.get_next_action())
    if agent1.actions:
        agent1.render_step(env, agent1.get_next_action())
    if agent2.actions:
        agent2.render_step(env, agent2.get_next_action())
    if agent3.actions:
        agent3.render_step(env, agent3.get_next_action())
   
    # render the cam
    env.render(env.cam_mode)

# Enter main event loop
pyglet.clock.schedule_interval(update, 1.0 / (env.unwrapped.frame_rate))
pyglet.app.run()

env.close()


    
