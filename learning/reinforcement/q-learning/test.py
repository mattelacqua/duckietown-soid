"""Testing the agent"""
import os
import sys
import time
from datetime import timedelta

# Learning things
import gym

# Environment
from gym_duckietown.envs import DuckietownEnv
from gym_duckietown.dl_utils import Action


# Logging
from gym_duckietown import logger 

# Utils / Event Wrappers
import gym_duckietown.utils as utils
import gym_duckietown.event_wrappers as event


from learn_types import *

# Test our learning
def test(args):

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
    
    # Init Q Table
    model = QTable(read_model(args.test_model_path))

    finishes = 0
    collisions = 0
    max_steps = 0
    offroads = 0
    rewards = 0
    steps = 0
    for i in range(1, args.num_iterations):
        # Reset the state
        env.reset()
        done = False

        # Set reward profile for agent 0
        env.agents[0].reward_profile = args.reward_profile
        env.agents[0].q_table = model

        # Learn until episode over
        epochs = 0
        while not done:

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
                    # Get initial State (Will be the row of the model)
                    agent.proceed(env, use_model=True, model=agent.q_table, state=agent.get_learning_state(env))
                    #print(agent.q_state)
                    #print(agent.learning_state)
                    #agent.proceed(env, good_agent=True)
                else:
                    agent.proceed(env, good_agent=True)
                

            env.step(learning=True)
            reward = env.agents[0].reward
            done = env.agents[0].done
            info = env.agents[0].misc
            done_code = info['done_code']

            reward, bad_actions = reward
            rewards += reward

            if done_code == 'offroad':
                offroads += 1
            elif done_code == 'finished':
                finishes += 1
            elif done_code == 'max-steps-reached':
                max_steps += 1
            elif done_code == 'collision':
                collisions += 1 
            if args.render_steps_test > 0 and epochs % args.render_steps_test == 0:
                env.render(mode=args.cam_mode)
            epochs += 1
        steps += env.agents[0].step_count
        print(f"Successes: {finishes} Collisions: {collisions} Max Steps: {max_steps} Offroad: {offroads} Avg_Reward: {rewards/i+1} Avg_Steps: {steps/i+1}")
            

def read_model(path):
        
    model = path

    # Read new model into a q table
    inp = open(model, 'r', os.O_NONBLOCK)
    table = []
    for line in inp.readlines():
        line.strip()
        table.append(list(float(i) for i in line.split(",")))
    inp.close()
    return table



# Main - Get arguments and train using Q learning
if __name__ == "__main__":

    # Parse arguments
    if len(sys.argv) >= 2:
        config_name = sys.argv[1]
    else: 
        print("Give a configuration name as an argument")
        exit()

    args = utils.get_args_from_config(config_name)

    # Test 
    start = time.time()
    test(args)
    elapsed = time.time() - start
    print(f"Elapsed Testing Time: {str(timedelta(seconds=elapsed))}")
    print(f"Model: {args.reward_profile}")
