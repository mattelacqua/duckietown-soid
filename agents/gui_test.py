#!/usr/bin/env python
# manual

"""
This script uses the ite_move library to make a right turn through an intersection
"""
from PIL import Image
import argparse
import sys
import time

import gym
import numpy as np
import pyglet
from pyglet.window import key, mouse

from gym_duckietown.envs import DuckietownEnv

# Includes all important moving functions for if then else agents
import gym_duckietown.agents

# Web gui stuff
import os
import subprocess

# Logging
from gym_duckietown import logger 
from webserver.gui_utils import unserialize


# Args
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
parser.add_argument("--verbose", action="store_true", help="Log agent information")
args = parser.parse_args()

# Build Env
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
        full_transparency=True,
        verbose=args.verbose
    )
else:
    env = gym.make(args.env_name)

# Verbose
verbose = args.verbose
# Start up env
env.reset()
env.render(args.cam_mode)

# Start up the webserver
subprocess.Popen(["python3","webserver/server.py"])

# Gui Stuff
@env.unwrapped.window.event
def on_key_press(symbol, modifiers):
    """
    This handler processes keyboard commands that
    control the simulation
    """

    if symbol == key.BACKSPACE or symbol == key.SLASH:
        env.reset()
        env.render()
    elif symbol == key.PAGEUP:
        env.unwrapped.cam_angle[0] = 0
    elif symbol == key.ESCAPE:
        env.close()
        sys.exit(0)

@env.unwrapped.window.event
def on_mouse_press(x, y, button, modifiers):
    """
    This handler processes keyboard commands that
    control the simulation
    """
    print("Mouse clicked at {0}, {1}".format(x, y))
    pyglet.clock.unschedule(update)
    pyglet.clock.schedule_interval(pause, 1.0 / (env.unwrapped.frame_rate))


    # Take a screenshot
    # UNCOMMENT IF NEEDED - Skimage dependency
    # elif symbol == key.RETURN:
    #     print('saving screenshot')
    #     img = env.render('rgb_array')
    #     save_img('screenshot.png', img)


# Register a keyboard handler
key_handler = key.KeyStateHandler()
mouse_handler = mouse.MouseStateHandler()
env.unwrapped.window.push_handlers(key_handler)

# Webserver handler
fifo_in = 'webserver/webserver.out'
inp = open(fifo_in, 'rb', os.O_NONBLOCK)

# Pause on space, can enter gui here and change things maybe????
def pause(dt):
    global inp
    gui_input = unserialize(inp)
    gui_input.handle_input(env)

    # Render any changes
    env.render(env.cam_mode)



    if key_handler[key.SPACE]:
        print("Unpausing")
        pyglet.clock.unschedule(pause)
        pyglet.clock.schedule_interval(update, 1.0 / (env.unwrapped.frame_rate))

          

def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    # Get the agents
    agent0 = env.agents[0] 
    agent1 = env.agents[1] 

    speed0 = 0.4
    speed1 = 0.2
    turn = 'Left'

    # Pause on Space
    if key_handler[key.SPACE]:
        print("Pausing")
        pyglet.clock.unschedule(update)
        pyglet.clock.schedule_interval(pause, 1.0 / (env.unwrapped.frame_rate))
            
    # If we are not handling a sequence already, try for agent 0
    if not agent0.actions:
        if agent0.intersection_detected(env):
            agent0.add_actions(agent0.handle_intersection(env, choice=turn, forward_step=speed0))
        else: 
            agent0.add_actions(agent0.move_forward(env, forward_step=speed0))

    # If we are not handling a sequence already, try for agent 1
    if not agent1.actions:
        if agent1.intersection_detected(env):
            agent1.add_actions(agent1.handle_intersection(env, choice=turn, forward_step=speed1))
        else: 
            agent1.add_actions(agent1.move_forward(env, forward_step=speed1))

    # Render each agent's next move
    if agent0.actions:
        agent0.render_step(env, agent0.get_next_action())
    if agent1.actions:
        agent1.render_step(env, agent1.get_next_action())
       
    # render the cam
    env.render(env.cam_mode)

if __name__ == '__main__':
    # Test the web server
    print(__name__)


    # Enter main event loop
    pyglet.clock.schedule_interval(update, 1.0 / (env.unwrapped.frame_rate))
    pyglet.app.run()

    env.close()


        
