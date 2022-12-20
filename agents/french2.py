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
    
    agent = env.agents[0]
    agent.turn_choice = 'Left'
    agent.curve = agent.get_curve(env)
    #print(agent.turn_choice)

    # Learn until episode over
    while True:

        lane_pose = env.get_lane_pos2(agent.cur_pos, agent.cur_angle)
        distance_to_road_center = lane_pose.dist
        angle_from_straight_in_rads = lane_pose.angle_rad

        ###### Commencez à remplir le code ici.
        k_p = 10
        k_d = 1

        # La vitesse est une valeur entre 0 et 1 (correspond à une vitesse réelle de 0 à 1,2m/s)

        vitesse = 0.44  # You should overwrite this value
        # l'angle du volant, c'est-à-dire le changement d'angle de la voiture en rads/s
        braquage = (
            k_p * distance_to_road_center + k_d * angle_from_straight_in_rads
        )  # You should overwrite this value

        ###### Fini à remplir le code ici
        print(braquage)
        action = np.array([vitesse, braquage]) , 1
        agent.render_step(env, action)
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
