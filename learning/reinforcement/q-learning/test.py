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
    
    # Init Q Table
    model = QTable(read_model(args.model_dir, args.reward_profile, args.model_num))

    for i in range(1, args.num_iterations):
        # Reset the state
        env.reset()
        done = False

        # Learn until episode over
        while not done:

            # Get initial State (Will be the row of the model)
            state = env.agents[0].get_learning_state(env)

            # Step each agent after choosing an action
            for agent in env.agents:

                # If not in the middle of an action, get one
                if not agent.actions:
                    if agent.intersection_detected(env):
                        agent.add_actions(agent.handle_intersection(env, learning=True))
                    else: 
                        agent.add_actions(agent.move_forward(env))

                # Save state and info for agent 0
                if agent.agent_id == "agent0":
                    agent.proceed(env, learning=True, model=model, state=state)
                    _, _, done, _ = env.step(agent.get_next_action(), agent, learning=True)
                    if done:
                        break
                else:
                    agent.proceed(env,good_agent=True)
                    env.step(agent.get_next_action(), agent, learning=True)

            env.render(mode=args.cam_mode)
            

def read_model(directory, reward_profile, model_number):
        
    profile = ""
    if reward_profile == 0:
        profile = "pathological"
    elif reward_profile == 1:
        profile = "impatient"
    elif reward_profile == 2:
        profile = "defensive"

    model = directory + profile + "/" + "episodebatch_" + str(model_number)

    # Read new model into a q table
    inp = open(model, 'r', os.O_NONBLOCK)
    table = []
    for line in inp.readlines():
        line.strip()
        table.append(list(float(i) for i in line.split(",")))
    inp.close()
    print(table)
    return table



# Main - Get arguments and train using Q learning
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Environment parse
    env_args = utils.get_args_from_command_line(parser)

    # Q learning Args
    parser.add_argument("--num-iterations", default=100, type=int)  # Nummber of episodes
    parser.add_argument("--model-dir", type=str, default="learning/reinforcement/q-learning/models/")
    parser.add_argument("--model-num", type=int, default=0)
    parser.add_argument("--reward-profile", type=int, default=2)

    args = parser.parse_args()

    # Test 
    test(args)
