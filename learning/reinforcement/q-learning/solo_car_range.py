"""Training the agent"""
import argparse
import os
import shutil
import random
import sys
import time

# Learning things
import gym
import numpy as np

from gym_duckietown.envs import DuckietownEnv
from gym_duckietown.dl_utils import Action

# Includes all important moving functions for if then else agents
import gym_duckietown.agents

# Logging
from gym_duckietown import logger 

# Utils / Event Wrappers
import gym_duckietown.utils as utils
import gym_duckietown.event_wrappers as event

import socketio

from learn_types import *
from gym_duckietown import dl_utils
import json
def test(args):

    # Make the environment
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
            num_random_agents=args.num_random_agents,
            full_transparency=True,
            verbose=args.verbose
        )
    else:
        env = gym.make(args.env_name)

    # Start up env
    env.reset()
    
    steps = {}
    steps_min = {}
    steps_max = {}
    lower_bound = 0.30
    upper_bound = 0.70
    a = lower_bound

    while a <= upper_bound:
        steps[a] = []
        steps_min[a] = 1500 
        steps_max[a] = 0 
        inc = a + 0.01
        a = round(inc, 2)

    for i in range(1, args.num_iterations):
        if i % 100 == 0:
            print(f"Iteration {i}")
        # Reset the state
        env.reset()
        done = False
        #print(f"forward_step {env.agents[0].forward_step}")
        agent = env.agents[0]

        # Learn until episode over
        while not done:

            # If not in the middle of an action, get one
            if not agent.actions:
                if agent.intersection_detected(env):
                    agent.add_actions(agent.handle_intersection(env, learning=True))
                else: 
                    agent.add_actions(agent.move_forward(env))


            agent.proceed(env,good_agent=True)
            _, _, done, misc = env.step(agent.get_next_action(), agent, learning=True)
            done_code = misc['done_code']
            if done_code == 'finished':
                steps[agent.forward_step].append(agent.step_count)

            #env.render(mode=args.cam_mode)

    for (key, value) in steps.items():
        print(f"Forward Step: {key} Values {value}")
        steps_min[key] = min(value) if value else None
        steps_max[key] = max(value) if value else None
    

    
    with open("learning/reinforcement/q-learning/solo/solo_runs.json", "w") as write_file:
        json.dump(steps, write_file, indent=4)
    
    #with open("solo_mins.json", "w") as write_file:
    with open("learning/reinforcement/q-learning/solo/solo_mins.json", "w") as write_file:
        json.dump(steps_min, write_file, indent=4)

    with open("learning/reinforcement/q-learning/solo/solo_maxs.json", "w") as write_file:
    #with open("solo_maxs.json", "w") as write_file:
        json.dump(steps_max, write_file, indent=4)
    
# Main - Get arguments and train using Q learning
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Environment parse
    env_args = utils.get_args_from_command_line(parser)

    # Q learning Args
    parser.add_argument("--num-iterations", default=100, type=int)  # Nummber of episodes
    parser.add_argument("--reward-profile", type=int, default=2)

    args = parser.parse_args()

    # Test 
    test(args)
