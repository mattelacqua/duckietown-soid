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
def train(args):
       # Hyperparameters
    alpha = args.alpha
    gamma = args.gamma
    epsilon = args.epsilon

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

    # Verbose
    verbose = args.verbose

    # Start up env
    env.reset()
    
    # For plotting metrics
    all_epochs = []
    all_penalties = []

    # Init Q Table
    q_table = QTable().qt

    print("Beginning Training.")
    for i in range(1, args.num_episodes):
        alpha = alpha * (1 - (i / args.num_episodes))
        epsilon = args.epsilon * (1 - (i / args.num_episodes)) 
        gamma = gamma
        # Reset the state
        env.reset()
        # Set reward profile for agent 0
        env.agents[0].reward_profile = args.reward_profile
        print(f"Agent 0 is turning: {env.agents[0].turn_choice}")

        epochs, penalties, reward, = 0, 0, 0
        done = False

        # Learn until episode over
        while not done:

            # Get initial State (Will be the row of the model)
            #print(f"GETTING INIT STATE in epoch {epochs}")
            #print(f"{env.agents[0].cur_pos}")
            state = env.agents[0].get_learning_state(env)
            #print(f"DONE")

            if random.uniform(0, 1) < epsilon:
                # Explore action space
                action = random.choice([0, 1])
            else:
                action = np.argmax(q_table[state]) # Exploit learned values

            # Step each agent after choosing an action
            print(f"Step = {env.agents[0].step_count}")
            #time.sleep(0.05)
            for agent in env.agents:
                # If not in the middle of an action, get one
                if not agent.actions:
                    if agent.intersection_detected(env):
                        print(f"{agent.agent_id} {agent.color} {agent.get_direction(env)} has detecting intersection.")
                        agent.add_actions(agent.handle_intersection(env))
                    else: 
                        agent.add_actions(agent.move_forward(env))

                # Check if we should proceed or not
                agent.proceed(env,good_agent=True)


                # Save state and info for agent 0
                #if agent.has_right_of_way(env) and (agent.in_intersection(env) or agent.at_intersection_entry(env)):
                    #print(f"{agent.agent_id} {agent.color} {agent.get_direction(env)} has right of way.")

                _, _, done, _ = env.step(agent.get_next_action(), agent, learning=True)
                if done:
                    break
            
            epochs += 1
            env.render(mode=args.cam_mode)
            
def write_model(directory, reward_profile, episode_batch, model):
        
    profile = ""
    if reward_profile == 0:
        profile = "pathological"
    elif reward_profile == 1:
        profile = "impatient"
    elif reward_profile == 2:
        profile = "defensive"

    model_save = directory + profile + "/" + "episodebatch_" + str(episode_batch)

    # Delete old files
    if episode_batch == 100:
        for filename in os.listdir(directory + profile):
            file_path = os.path.join(directory + profile, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Write new model
    out = open(model_save, 'w', os.O_NONBLOCK)
    for i in range(0, STATES):
        out.write("[" + str(model[i][0]) + "] [" + str(model[i][1]) + "]\n")
    out.close()


# Main - Get arguments and train using Q learning
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Environment parse
    env_args = utils.get_args_from_command_line(parser)

    # Q learning Args
    parser.add_argument("--eval_freq", default=5e3, type=float)  # How often (time steps) we evaluate
    parser.add_argument("--max_timesteps", default=1e6, type=float)  # Max time steps to run environment for
    parser.add_argument("--save_models", action="store_true", default=True)  # Whether or not models are saved
    parser.add_argument("--alpha", default=0.1, type=float)  # Alpha learning rate 
    parser.add_argument("--gamma", default=0.6, type=float)  # Gamma preference to short term reward
    parser.add_argument("--epsilon", default=0.35, type=float)  # Epsilon for egreedy q learning 
    parser.add_argument("--discount", default=0.99, type=float)  # Discount factor
    parser.add_argument("--num-episodes", default=100001, type=int)  # Nummber of episodes
    parser.add_argument("--reward-profile", default=2, type=int)  # Rewards (0 = pathological, 1= impatient, 2= defensive)
    parser.add_argument("--model-dir", type=str, default="learning/reinforcement/q-learning/models/")

    args = parser.parse_args()

    # Train 
    train(args)
