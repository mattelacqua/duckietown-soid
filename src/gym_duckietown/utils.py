# coding=utf-8
import os
import configparser
from ctypes import c_char_p, cast
from typing import Dict
import json
import pyglet
pyglet.options["headless"] = True
from pyglet import gl

__all__ = ["get_graphics_information"]

def get_subdir_path(sub_dir):
    # Get the directory this module is located in
    abs_path_module = os.path.realpath(__file__)
    module_dir, _ = os.path.split(abs_path_module)

    dir_path = os.path.join(module_dir, sub_dir)

    return dir_path


def get_file_path(sub_dir, file_name, default_ext):
    """
    Get the absolute path of a resource file, which may be relative to
    the gym_duckietown module directory, or an absolute path.

    This function is necessary because the simulator may be imported by
    other packages, and we need to be able to load resources no matter
    what the current working directory is.
    """

    assert "." not in default_ext
    assert "/" not in default_ext

    # If this is already a real path
    if os.path.exists(file_name):
        return file_name

    subdir_path = get_subdir_path(sub_dir)
    file_path = os.path.join(subdir_path, file_name)

    if "." not in file_name:
        file_path += "." + default_ext

    return file_path

# Args
def get_args_from_config(config_name: str):
    params = configparser.ConfigParser()
    print(config_name)
    params.read(config_name)
    class Args:
        # Logging 
        verbose: bool
        seed: int

        # Randomization
        domain_rand: bool
        dynamics_rand: bool
        distortion: bool
        camera_rand: bool
        
        # Simulator settings
        env_name: str
        map_name: str
        draw_curve: bool
        draw_bbox: bool
        frame_skip: int
        cam_mode: str

        # Agent Settings
        num_random_agents: int
        safety_factor: float

        # Training Settings
        save_models: bool
        model_dir: str
        alpha: float
        learning_rate_decay: float
        gamma: float
        epsilon: float
        num_episodes: int
        num_iterations: int
        model_num: int
        reward_profile: int
        render_steps: int

        def __init__(self):
            # Logging
            self.verbose=params.getboolean('LOGGING', 'VERBOSE')

            # Randomization
            self.seed=params.getint('RANDOMIZATION', 'SEED')
            self.domain_rand=params.getboolean('RANDOMIZATION', 'DOMAIN_RAND')
            self.dynamics_rand=params.getboolean('RANDOMIZATION', 'DYNAMICS_RAND')
            self.distortion=params.getboolean('RANDOMIZATION', 'DISTORTION')
            self.camera_rand=params.getboolean('RANDOMIZATION', 'CAMERA_RAND')
            self.camera_rand=params.getboolean('RANDOMIZATION', 'CAMERA_RAND')

            # Simulator SEtup
            self.env_name=str(params.get('SETUP', 'ENV'))
            self.map_name=str(params.get('SETUP', 'MAP'))
            self.draw_curve=params.getboolean('SETUP', 'DRAW_CURVE')
            self.draw_bbox=params.getboolean('SETUP', 'DRAW_BBOX')
            self.frame_skip=params.getint('SETUP', 'FRAME_SKIP')
            self.cam_mode=str(params.get('SETUP', 'CAM_MODE'))

            # Agents
            self.num_random_agents=params.getint('AGENTS', 'NUM_RANDOM_AGENTS')
            self.safety_factor=params.getfloat('AGENTS', 'SAFETY_FACTOR')

            # Learning
            self.save_models=params.getboolean('LEARNING', 'SAVE_MODELS')
            self.model_dir=str(params.get('LEARNING', 'MODEL_DIR'))
            self.alpha=params.getfloat('LEARNING', 'ALPHA')
            self.learning_rate_decay=params.getfloat('LEARNING', 'LEARNING_RATE_DECAY')
            self.gamma=params.getfloat('LEARNING', 'GAMMA')
            self.epsilon=params.getfloat('LEARNING', 'EPSILON')
            self.num_episodes=params.getint('LEARNING', 'NUM_EPISODES')
            self.num_iterations=params.getint('LEARNING', 'NUM_ITERATIONS')
            self.model_num=params.getint('LEARNING', 'MODEL_NUM')
            self.reward_profile=params.getint('LEARNING', 'REWARD_PROFILE')
            self.render_steps=params.getint('LEARNING', 'RENDER_STEPS')
    
    args = Args()
    return args

def get_graphics_information() -> Dict:
    options = {
        "vendor": gl.GL_VENDOR,
        "renderer": gl.GL_RENDERER,
        "version": gl.GL_VERSION,
        "shading-language-version": gl.GL_SHADING_LANGUAGE_VERSION,
        # 'extensions': gl.GL_EXTENSIONS
    }

    results = {}
    for o, code in options.items():
        a = gl.glGetString(code)
        b: bytes = cast(a, c_char_p).value
        res = b.decode()
        results[o] = res
    return results

