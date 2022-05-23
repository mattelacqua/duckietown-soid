#!/usr/bin/env python
# manual

"""
This script allows you to manually control the simulator or Duckiebot
using the keyboard arrows.
"""
from turtle import back, forward
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
        draw_curve=args.draw_curve,
        draw_bbox=args.draw_bbox,
        domain_rand=args.domain_rand,
        frame_skip=args.frame_skip,
        distortion=args.distortion,
        camera_rand=args.camera_rand,
        dynamics_rand=args.dynamics_rand,
    )
else:
    env = gym.make(args.env_name)

env.reset()
env.render(args.cam_mode)


# Recursive function for undoing an action
def undo_action(forward_step, direction, action, done):
    # base case
    if done == False:
        return
    else:
        # If forward move back, if backward move forward
        if direction == 1.0:
            action[0] -= forward_step
        else:
            action[0] += forward_step

        # reevaluate step function, rerender, recursive call
        obs, reward, done, info = env.step(action)
        env.render(args.cam_mode)
        undo_action(forward_step, direction, action, done)
        


def update():
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    wheel_distance = 0.102
    min_rad = 0.08
    forward_step = 0.44
    turn_step = 1.0

    # just to create endless while loop
    looper = 0

    while looper == 0:

        # initialize "done" variable
            # False when on road
            # True when hits something
        done = False

        # move forward while no obstacle in the way
        while not done:
            # initialize action array
            action = np.array([0.0, 0.0])

            print("Forward Step")
            action += np.array([forward_step, 0.0])

            v1 = action[0]
            v2 = action[1]
            # Limit radius of curvature
            if v1 == 0 or abs(v2 / v1) > (min_rad + wheel_distance / 2.0) / (min_rad - wheel_distance / 2.0):
                # adjust velocities evenly such that condition is fulfilled
                delta_v = (v2 - v1) / 2 - wheel_distance / (4 * min_rad) * (v1 + v2)
                v1 += delta_v
                v2 -= delta_v

            action[0] = v1
            action[1] = v2

            obs, reward, done, info = env.step(action)
            print(done)
            print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))

            env.render(args.cam_mode)

            
        # If we hit something
        if done:
            # undo the last action so we don't get stuck looping on a single error
            undo_action(forward_step, 1, action, done)

            # backup and rotate to the right for 30 steps
            backup = 0
            while backup != 30:

                # reinitialize so no values from forward while loop
                action = np.array([0.0, 0.0])

                # backup and rotate to the right
                print("Backward Right Step")
                action -= np.array([forward_step, 0.0])
                action -= np.array([0.0, turn_step])

                backup += 1

                v1 = action[0]
                v2 = action[1]
                # Limit radius of curvature
                if v1 == 0 or abs(v2 / v1) > (min_rad + wheel_distance / 2.0) / (min_rad - wheel_distance / 2.0):
                    # adjust velocities evenly such that condition is fulfilled
                    delta_v = (v2 - v1) / 2 - wheel_distance / (4 * min_rad) * (v1 + v2)
                    v1 += delta_v
                    v2 -= delta_v

                action[0] = v1
                action[1] = v2

                obs, reward, done, info = env.step(action)
                print(done)
                print("step_count = %s, reward=%.3f" % (env.unwrapped.step_count, reward))

                env.render(args.cam_mode)

                # If we hit something while backing up
                if done:
                    # undo last action
                    undo_action(forward_step, 0, action, done)
                    # break to first/forward while loop again
                    break

update()

env.close()
