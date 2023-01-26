"""Training the agent"""
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
            max_agents=args.max_agents,
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

        # Learn until episode over
        while not done:
            # Step each agent after choosing an action
            for agent in env.agents:

                # If not in the middle of an action, get one
                if not agent.actions:
                    if agent.intersection_detected(env):
                        agent.add_actions(agent.handle_intersection(env))
                    else: 
                        agent.add_actions(agent.move_forward(env))

                agent.proceed(env,good_agent=True)

            env.step(learning=True)
            done = env.agents[0].done 
            if (agent.step_count % args.render_steps == 0):
                env.render(mode=args.cam_mode)
            
if __name__ == '__main__':
    args = utils.get_args_from_config(sys.argv[1])
    test(args)