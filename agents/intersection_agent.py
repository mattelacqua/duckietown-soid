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
args = parser.parse_args()

if args.env_name and args.env_name.find("Duckietown") != -1:
    env = DuckietownEnv(
        seed=args.seed,
        map_name=args.map_name,
        cam_mode=args.cam_mode,
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

def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    # Get the agents
    agent0 = env.agents[0] 

    speed0 = 0.4
    turn = None # Set to 'Right' 'Left' 'Straight' or None for nodeterminism 

    # If we are not handling a sequence already, try for agent 0
    if not agent0.actions:
        if agent0.intersection_detected(env):
            agent0.add_actions(agent0.handle_intersection(env, choice=turn, forward_step=speed0))
        else: 
            agent0.add_actions(agent0.move_forward(env, forward_step=speed0))

    # Render each agent's next move
    if agent0.actions:
        agent0.render_step(env, agent0.get_next_action())  

        # render the cam
    env.render(env.cam_mode)

# Enter main event loop
pyglet.clock.schedule_interval(update, 1.0 / (env.unwrapped.frame_rate))
pyglet.app.run()

env.close()



