#!/usr/bin/env python
# manual

"""
This script uses the ite_move library to make a right turn through an intersection
"""
from PIL import Image
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
import multiprocessing

# Logging
from gym_duckietown import logger 
from webserver.gui_utils import unserialize, init_server

# Utils / Event Wrappers
import gym_duckietown.utils as utils
import gym_duckietown.event_wrappers as event

# Parse args
args = utils.get_args_from_command_line()

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

# Start up the webserver
webserver = subprocess.Popen(["python3","webserver/server.py"])

# Render
env.render(args.cam_mode)

# Handle Key Presses 
@env.unwrapped.window.event
def on_key_press(symbol, modifiers):
    event.on_key_press(symbol, modifiers, env)

@env.unwrapped.window.event
def on_mouse_press(x, y, button, modifiers):
    event.on_mouse_press(x, y, button, modifiers, update, pause)
    
# Register a keyboard handler
key_handler = key.KeyStateHandler()
mouse_handler = mouse.MouseStateHandler()
env.unwrapped.window.push_handlers(key_handler)

# Webserver handler
fifo_in = 'webserver/webserver.out'
fifo_out = 'webserver/webserver.in'
inp = open(fifo_in, 'rb', os.O_NONBLOCK)
out = open(fifo_out, 'wb', os.O_NONBLOCK)

# Feed agent information to webserver
init_server(out, env)

# Pause on space, keep trying to get info from webserver, render and update accordingly
def pause(dt):
    global inp
    state = "pause"
    # While still getting input
    while state == "pause":
        gui_input = unserialize(inp)
        # Handle input, Modify env, see functions in gui_utills. Returns true on button for resume
        if gui_input:
            state = gui_input.handle_input(env)
            if state == "quit":
                print("Killing Webserver")
                webserver.kill()
                print("Killing Simulator")
                exit()

            elif state == "run":
                print("Resuming Simulationr")
        # Render any changes from last thing serialized
        env.render(env.cam_mode)

    # Reset with a webserver reset
    env.reset(webserver_reset=True)
    env.render(env.cam_mode)

    # Unschedule pause and resume rendering
    pyglet.clock.unschedule(pause)
    pyglet.clock.schedule_interval(update, 1.0 / (env.unwrapped.frame_rate))

def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """

    # Handle input, Modify env, see functions in gui_utills. Returns true on button for resume
    """gui_input = multiprocessing.Process(target=unserialize, args=(inp))
    gui_input.start()
    gui_input.join(timeout=1)
    gui_input.terminate()

    if gui_input:
        state = gui_input.handle_input(env)
        if state == "quit":
            print("Killing Webserver")
            webserver.kill()
            print("Killing Simulator")
            exit()"""



    # Get the agents
    agent0 = env.agents[0] 
    agent1 = env.agents[1] 

    speed0 = 0.4
    speed1 = 0.2
    turn = 'Left'

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

    # Enter main event loop
    pyglet.clock.schedule_interval(update, 1.0 / (env.unwrapped.frame_rate))
    pyglet.app.run()

    env.close()


        
