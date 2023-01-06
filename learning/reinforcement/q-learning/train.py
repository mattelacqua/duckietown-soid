"""Training the agent"""
import sys
import os
import shutil
import random

# Learning things
import gym
import numpy as np

# Environment
from gym_duckietown.envs import DuckietownEnv

# Logging
from gym_duckietown import logger 

# Utils / Event Wrappers
import gym_duckietown.utils as utils
import gym_duckietown.event_wrappers as event

# Types 
from learn_types import *
import matplotlib.pyplot as plt

# Train the agent using q learning
def train(args):

    # Hyperparameters
    alpha = args.alpha
    gamma = args.gamma
    epsilon = args.epsilon
    learning_rate_decay = args.learning_rate_decay

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
            num_random_agents=args.num_random_agents,
            max_agents=args.max_agents,
            full_transparency=True,
            verbose=args.verbose
        )
    else:
        env = gym.make(args.env_name)

    # Start up env
    env.reset()
    
    # For plotting metrics
    all_epochs = []
    all_penalties = []
    avg_rewards = []
    avg_rewards_index = []
    rewards = []

    # Init Q Table
    q_table = QTable().qt
    total_stats = []
    learning_rates = []
    state_visits = []
    # learning rates and visits per state action
    for i in range (0, 1024):
        sa = []
        lr = []
        for j in range (0,2): # For the actions
            sa.append(0)
            lr.append(alpha)
        learning_rates.append(lr)
        state_visits.append(sa)

    print("Beginning Training.")
    for i in range(1, args.num_episodes):
        epsilon = args.epsilon * (1 - (i / args.num_episodes)) 
        if epsilon < 0.05:
            epsilon = 0.05
        gamma = gamma

        # Reset the state
        env.reset()

        # Set reward profile for agent 0
        env.agents[0].reward_profile = args.reward_profile

        epochs, penalties, reward, = 0, 0, 0
        done = False

        # Set the rewards to be 0
        if i % 100 == 0 and i > 1000:
            avg_rewards.append(sum(rewards)/len(rewards))
            avg_rewards_index.append(i)
            rewards = []


        # Learn until episode over
        reward_sum = 0
        bad_actions_sum = 0
        while not done:

            # Get initial State (Will be the row of the model)
            state = env.agents[0].get_learning_state(env)

            if random.uniform(0, 1) < epsilon:
                # Explore action space
                action = random.choice([0, 1])
            else:
                action = np.argmax(q_table[state]) # Exploit learned values

            # Prep each agent by choosing an action
            for agent in env.agents:

                # If not in the middle of an action, get one
                if not agent.actions:
                    if agent.intersection_detected(env):
                        agent.add_actions(agent.handle_intersection(env, learning=True))
                    else: 
                        agent.add_actions(agent.move_forward(env))

                # Save state and info for agent 0
                if agent.agent_id == "agent0":
                    agent.handle_proceed(bool(action))
                    # If the handle proceed needs an initial action, add it
                    if not agent.actions:
                        agent.add_actions(agent.move_forward(env))
                else: # For everyone else just step
                    agent.proceed(env,good_agent=True)
            

            # Step the env
            env.step(learning = True)
            
            # Get info from the step
            next_state = env.agents[0].q_state
            reward = env.agents[0].reward
            done = env.agents[0].done 
            info = env.agents[0].misc 

            reward, bad_actions = reward
            reward_sum += reward
            bad_actions_sum += bad_actions

            # Calculate and set the new q table stuff
            old_value = q_table[state][action]
            if not next_state:
                next_max = 0 # If end of episode we have 0 for our next max stateval
            else:
                next_max = np.max(q_table[next_state])
            
            alpha = learning_rates[state][action]
            state_visits[state][action] += 1
            new_value = alpha * (reward + gamma * next_max - old_value)
            
            # If we have visited the state 100 times, drop the learning rate of it
            if state_visits[state][action] % (int(args.num_episodes / 10)) == 0:
                learning_rates[state][action] *= learning_rate_decay

            q_table[state][action] += new_value
            
            if reward <= -1000:
                penalties += 1
            
            rewards.append(reward)

            epochs += 1

            # Render if we choose to
            if args.render_steps:
                if epochs % args.render_steps == 0:
                    env.render(mode=args.cam_mode)
            
        # Do bookeeping
        stats = {}
        stats['Episode'] = i
        stats['Result'] = info['done_code']
        stats['Forward_Step'] = env.agents[0].forward_step
        stats['Total_Steps'] = env.agents[0].step_count
        stats['Reward'] = reward_sum
        stats['Bad_Actions'] = bad_actions_sum
        stats['Alpha'] = alpha
        stats['Epsilon'] = epsilon
        stats['Avg_rps'] = reward_sum/epochs
        print(stats)
        total_stats.append(stats)

        if args.save_models:
            if i % 100 == 0 or i == (args.num_episodes - 1):
                write_model(args.model_dir, args.reward_profile, i, q_table)
                print(f"Batch Episodes: {i}")

    print("Training finished.\n")

    print(avg_rewards)
    plt.plot(avg_rewards_index, avg_rewards)
    plt.ylabel('Rewards')
    plt.xlabel('Episode #')
    plt.show()

# Write the model
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
        out.write(str(model[i][0]) + "," + str(model[i][1]) + "\n")
    out.close()


# Main - Get arguments and train using Q learning
if __name__ == "__main__":

    # Parse arguments
    if len(sys.argv) >= 2:
        config_name = sys.argv[1]
    else: 
        print("Give a configuration name as an argument")
        exit()

    args = utils.get_args_from_config(config_name)

    # Train 
    train(args)
