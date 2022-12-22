#!/usr/bin/env python
# manual

"""
This script uses the ite_move library to make a right turn through an intersection
"""
import time
import sys

import gym
import pyglet
from pyglet.window import key, mouse

from gym_duckietown.envs import DuckietownEnv

# Web gui stuff
import os

# Logging
from gym_duckietown import logger 
import webserver.gui_utils as gu 
from threading import Thread

# Utils / Event Wrappers
import gym_duckietown.utils as utils
import gym_duckietown.event_wrappers as event

import socketio

# Parse args
args = utils.get_args_from_config(sys.argv[1])

# Build Env
if args.env_name and args.env_name.find("Duckietown") != -1:
    env = DuckietownEnv(
        seed=args.seed,
        map_name=args.map_name,
        cam_mode=args.cam_mode,
        safety_factor=args.safety_factor,
        draw_curve=args.draw_curve,
        draw_bbox=args.draw_bbox,
        domain_rand=args.domain_rand,
        frame_skip=args.frame_skip,
        distortion=args.distortion,
        camera_rand=args.camera_rand,
        dynamics_rand=args.dynamics_rand,
        full_transparency=True,
        verbose=args.verbose,
        num_random_agents=args.num_random_agents
    )
else:
    env = gym.make(args.env_name)

# Verbose
verbose = args.verbose

# Start up env
env.reset()

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
fifo_log = 'webserver/webserver.log'

# CLEAR OLD STUFF
clear = open(fifo_in, 'wb').close()
clear = open(fifo_out, 'wb').close()
clear = open(fifo_log, 'wb').close()

# Write new stuff
out = open(fifo_out, 'wb', os.O_NONBLOCK)
inp = open(fifo_in, 'rb', os.O_NONBLOCK)
log = open(fifo_log, 'wb', os.O_NONBLOCK)

# Start up the webserver before reading so that it clears write file
webserver = gu.start_webserver()

# Set up initial agent speeds, turns and contols
#env.agents[0].forward_step = 0.44
#env.agents[1].forward_step = 0.22
#env.agents[2].forward_step = 0.00

#env.agents[0].turn_choice = "Left" 
#env.agents[0].curve = env.agents[0].get_curve(env)
#env.agents[1].turn_choice = "Straight" 
#env.agents[1].curve = env.agents[1].get_curve(env)
# Random is None which will be the 3rd agent

# Feed agent information to webserver
gu.init_server(0, out, env, None, get_map=True)

# Socket Connection
print("Connecting to Socket")
socket = socketio.Client()
while True:
    try:    socket.connect('http://127.0.0.1:5000', wait=True)
    except Exception as e: pass
    else:   break

# Pause on space, keep trying to get info from webserver, render and update accordingly
def pause(dt):
    global inp
    env.state = "pause"

    # Feed agent information to webserver
    gu.init_server(0, out, env, socket)

    # While still getting input
    while env.state == "pause":
        gui_input = list(gu.unserialize(inp))
        # Handle input, Modify env, see functions in gui_utills. Returns true on button for resume
        if gui_input:
            gui_input = gui_input[-1]
            env.state = gui_input.handle_input(env)
            gu.init_server(0, out, env, socket)
            if env.state == "quit":
                print("Killing Webserver")
                gu.init_server(0, out, env, socket, get_map=False) # Init to send the dead signal to 
                time.sleep(2)
                webserver.kill()
                print("Killing Simulator")
                socket.disconnect()
                exit()
            elif env.state == "run":
                print("Resuming Simulation")

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
    gui_input = list(gu.unserialize(inp))

    if gui_input:
        gui_input = gui_input[-1]
        state = gui_input.handle_input(env)
        if state == "quit":
            print("Killing Webserver")
            webserver.kill()
            print("Killing Simulator")
            exit()
        elif state == "pause":
            # Unschedule pause and resume rendering
            print("Pausing the Simulator")
            pyglet.clock.unschedule(update)
            pyglet.clock.schedule_interval(pause, 1.0 / (env.unwrapped.frame_rate))

    # Perform next agent action
    for agent in env.agents:
        # If we are not handling a sequence already, try for agent
        if not agent.actions:
            if agent.intersection_detected(env):
                agent.add_actions(agent.handle_intersection(env))
            else: 
                agent.add_actions(agent.move_forward(env))

        # Render agent's next move
        if agent.actions:
            agent.proceed(env,good_agent=True)
            agent.render_step(env, agent.get_next_action())

    # Log the info
    if env.agents[0].step_count % 10 == 0 or env.agents[0].step_count == 1:
        print("Logging")
        gu.init_server(1, log, env, socket)

    # render the cam
    env.render(env.cam_mode)

if __name__ == '__main__':

    # Enter main event loop
    pyglet.clock.schedule_interval(pause, 1.0 / (env.unwrapped.frame_rate))
    pyglet.clock.schedule_interval(gu.init_server, 1, out, env, socket)
    pyglet.app.run()

    env.close()


        
