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
from ite_move import *

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
    print("HERE")
    env = DuckietownEnv(
        seed=args.seed,
        map_name=args.map_name,
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

env.reset()
env.render(args.cam_mode)

    
def update():
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    wheel_distance = 0.102
    min_rad = 0.08
    forward_step = 0.44
    turn_step = 1.0

    action = np.array([0.0, 0.0])

    info = env.get_agent_info()
    tile_coords = info['Simulator']['tile_coords']
    current_tile = env._get_tile(tile_coords[0], tile_coords[1])

     # If we are at a 4 way
    if intersection_detected(wheel_distance, min_rad, forward_step, turn_step, action, env, args):
        handle_intersection(wheel_distance, min_rad, forward_step, turn_step, action, env, args)
    else:
        # Otherwise go straight
        action += np.array([forward_step, 0.0])

    # Refine action and do step
    action = limit_rad_curvature(wheel_distance, min_rad, forward_step, turn_step, action, env, args)
    obs, reward, done, info = env.step(action)
    print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))

    # If we hit something fail, otherwise render
    return render_step(done, env, args)


# Enter main event loop
keep_going = True
while keep_going:
    keep_going = update()

env.close()


    
