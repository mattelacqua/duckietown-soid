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
from gym_duckietown.agents import Agent
from gym_duckietown.utils import read_model
import webserver.gui_utils as gu 
from threading import Thread

# Utils / Event Wrappers
import gym_duckietown.utils as utils
import gym_duckietown.event_wrappers as event

import socketio
from learn_types import *

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
        num_random_agents=0,
        max_agents=args.max_agents
    )
else:
    env = gym.make(args.env_name)

# Verbose
verbose = args.verbose




# Initialize the agents for the scripted scenario
env.agents[0] = Agent(env, cur_pos=[1.6, 0, 2.6], cur_angle=1.57080, agent_id="agent0", color="blue")
env.agents.append(Agent(env, cur_pos=[0.5, 0, 1.6], cur_angle=0, agent_id="agent1", color="red"))

learn_agent = env.agents[0]
env_agent = env.agents[1]

learn_agent.agent_id = "agent0"
learn_agent.index = 0
learn_agent.forward_step = 0.44
learn_agent.turn_choice = 'Right' 
learn_agent.signal_choice = 'Right' 
learn_agent.curve = learn_agent.get_curve(env)
learn_agent.reward_profile = args.reward_profile

env_agent.agent_id = "agent1"
env_agent.index = 1
env_agent.forward_step = 0.44
env_agent.turn_choice = 'Right' 
env_agent.signal_choice = 'Right' 
env_agent.curve = env_agent.get_curve(env)

# Start up env
env.reset(webserver_reset=True)

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
fifo_in = 'src/webserver/webserver.out'
fifo_out = 'src/webserver/webserver.in'
fifo_log = 'src/webserver/webserver.log'

# CLEAR OLD STUFF
clear = open(fifo_in, 'w').close()
clear = open(fifo_out, 'w').close()
clear = open(fifo_log, 'w').close()

# Write new stuff
out = open(fifo_out, 'w', os.O_NONBLOCK)
inp = open(fifo_in, 'r', os.O_NONBLOCK)
log = open(fifo_log, 'w', os.O_NONBLOCK)

# Start up the webserver before reading so that it clears write file
webserver = gu.start_webserver()
node = gu.start_node()


# Feed agent information to webserver
gu.init_server(0, out, env, None, get_map=True)

# Socket Connection
print("Connecting to Socket")
socket = socketio.Client()
while True:
    try:    socket.connect('http://127.0.0.1:5001', wait=True)
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
        try:
            gui_input = list(gu.unserialize(inp))
        except:
            pass
        # Handle input, Modify env, see functions in gui_utills. Returns true on button for resume
        if gui_input:
            gui_input = gui_input[-1]
            env.state, input_return = gu.handle_input(env, gui_input)
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
            elif env.state == "query_result":
                print(input_return)
                env.state = 'pause'

        # Render any changes from last thing serialized
        env.render(mode=args.cam_mode)

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
        state, query_ret  = gu.handle_input(env, gui_input)
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
            if not agent.good_agent:
                agent.proceed(env, use_model=True, model=agent.q_table, state=agent.get_learning_state(env))
            else:
                agent.proceed(env,good_agent=True)

    env.step(learning=True)

    # Log the info
    #print(f"Logging Step {env.agents[0].step_count}")
    gu.init_server(1, log, env, socket)

    # render the cam
    env.render(mode=args.cam_mode)



if __name__ == '__main__':

    # Enter main event loop
    pyglet.clock.schedule_interval(pause, 1.0 / (env.unwrapped.frame_rate))
    pyglet.clock.schedule_interval(gu.init_server, 1, out, env, socket)
    pyglet.app.run()

    env.close()


        
