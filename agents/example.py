# Learning things
import gym
import sys

from gym_duckietown.envs import DuckietownEnv

# Logging
from gym_duckietown import logger 

# Utils / Event Wrappers
import gym_duckietown.utils as utils

# Test function
def test(args):

    # Make the environment
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
            full_transparency=True,
            verbose=args.verbose
        )
    else:
        env = gym.make(args.env_name)

    # Start up env
    env.reset()
    
    # For the number of iterations we want to test (this is just to see it again)
    for i in range(1, args.num_iterations):
        # Reset the state
        env.reset()

        done = False

        # Until one agent ends
        while not done:
            for agent in env.agents: 
                # If not in the middle of an action, get one
                if not agent.actions:
                    if agent.intersection_detected(env):
                        agent.add_actions(agent.handle_intersection(env))
                    else: 
                        agent.add_actions(agent.move_forward(env))

                agent.proceed(env,good_agent=True)

            # Render
            env.step()
            done = env.agents[0].done
            env.render(mode=args.cam_mode)
    
# Main - Get arguments and train using Q learning
if __name__ == "__main__":

    # Argument parse
    if len(sys.argv) >= 2:
        config_name = sys.argv[1]
    else: 
        print("Give a configuration name as an argument")
        exit()

    args = utils.get_args_from_config(config_name)

    # Test 
    test(args)
