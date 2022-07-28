# coding=utf-8
import os
import argparse


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
def get_args_from_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-name", default=None)
    parser.add_argument("--map-name", default="udem1")
    parser.add_argument("--distortion", default=False, action="store_true")
    parser.add_argument("--camera_rand", default=False, action="store_true")
    parser.add_argument("--draw-curve", action="store_true", help="draw the lane following curve")
    parser.add_argument("--draw-bbox", action="store_true", help="draw collision detection bounding boxes")
    parser.add_argument("--domain-rand", action="store_true", help="enable domain randomization")
    parser.add_argument("--dynamics_rand", action="store_true", help="enable dynamics randomization")
    parser.add_argument("--frame-skip", default=1, type=int, help="number of frames to skip")
    parser.add_argument("--seed", default=1, type=int, help="seed")
    parser.add_argument("--cam-mode", default="human", help="Camera modes: human, top_down, free_cam, rgb_array")
    parser.add_argument("--safety-factor", default=1.0, type=float, help="Minimum distance before collision detection")
    parser.add_argument("--num-agents", default=1.0, type=int, help="Number of Agents")
    parser.add_argument("--verbose", action="store_true", help="Log agent information")
    args = parser.parse_args()

    return args

