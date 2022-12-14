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

from gym_duckietown import dl_utils
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
    
    for i in range(1, args.num_iterations):
        # Reset the state
        env.reset()
        done = False
        #print(f"forward_step {env.agents[0].forward_step}")
        agent = env.agents[0]
        agent.turn_choice = 'Left'
        agent.curve = agent.get_curve(env)
        #print(agent.turn_choice)

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

            env.render(mode=args.cam_mode)
    
# Main - Get arguments and train using Q learning
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Environment parse
    env_args = utils.get_args_from_command_line(parser)

    # Q learning Args
    parser.add_argument("--num-iterations", default=100, type=int)  # Nummber of episodes

    args = parser.parse_args()

    # Test 
    test(args)
