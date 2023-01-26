import itertools
import os
import random
from collections import namedtuple
from ctypes import POINTER
from dataclasses import dataclass

import sys
import subprocess

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from typing import Any, cast, Dict, List, NewType, Optional, Sequence, Tuple, Union

import geometry
import geometry as g
import gym
import math
import numpy as np
import pyglet
import yaml
from geometry import SE2value
from gym import spaces
from gym.utils import seeding
from numpy.random.mtrand import RandomState
from pyglet import gl, image, window
from pyglet.gl import gluSphere, gluNewQuadric

from .map_format import(
    MapFormat1,
    MapFormat1Constants,
    MapFormat1Constants as MF1C,
    MapFormat1Object,
)

from duckietown_world import (
    get_DB18_nominal,
    get_DB18_uncalibrated,
    get_texture_file,
    SE2Transform,
)
from duckietown_world.gltf.export import get_duckiebot_color_from_colorname
from duckietown_world.resources import get_resource_path
from duckietown_world.world_duckietown.map_loading import get_transform
from . import logger
from .utils import get_graphics_information
from .collision import (
    agent_boundbox,
    generate_norm,
    intersects,
    safety_circle_intersection,
    safety_circle_overlap,
    tile_corners,
    intersects_single_obj,
)
from .distortion import Distortion
from .exceptions import InvalidMapException, NotInLane
from .graphics import (
    bezier_closest,
    bezier_draw,
    bezier_point,
    bezier_tangent,
    create_frame_buffers,
    gen_rot_matrix,
    load_texture,
    Texture,
)
from .objects import CheckerboardObj, DuckiebotObj, DuckieObj, TrafficLightObj, WorldObj
from .objmesh import get_mesh, MatInfo, ObjMesh
from .randomization import Randomizer
from .utils import get_subdir_path

from .agents import *

from PIL import Image



DIM = 0.5

TileKind = NewType("TileKind", str)


class TileDict(TypedDict):
    # {"coords": (i, j), "kind": kind, "angle": angle, "drivable": drivable})
    coords: Tuple[int, int]
    kind: TileKind
    angle: int
    drivable: bool
    texture: Texture
    color: np.ndarray
    curves: Any


@dataclass
class DoneRewardInfo:
    done: bool
    done_why: str
    done_code: str
    reward: float


@dataclass
class DynamicsInfo:
    motor_left: float
    motor_right: float


# Rendering window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Camera image size
DEFAULT_CAM_MODE = "top_down" 
DEFAULT_CAMERA_WIDTH = 640
DEFAULT_CAMERA_HEIGHT = 480

# Blue sky horizon color
BLUE_SKY = np.array([0.45, 0.82, 1])

# Color meant to approximate interior walls
WALL_COLOR = np.array([0.64, 0.71, 0.28])

# np.array([0.15, 0.15, 0.15])
GREEN = (0.0, 1.0, 0.0)
# Ground/floor color


# Angle at which the camera is pitched downwards
CAMERA_ANGLE = 19.15

# Camera field of view
# Note: robot uses Raspberri Pi camera module V1.3
# https://www.raspberrypi.org/documentation/hardware/camera/README.md
CAMERA_FOV_Y = 75

# Distance from camera to floor (10.8cm)
CAMERA_FLOOR_DIST = 0.108

# Forward distance between the camera (at the front)
# and the center of rotation (6.6cm)
CAMERA_FORWARD_DIST = 0.066

# Distance (diameter) between the center of the robot wheels (10.2cm)
WHEEL_DIST = 0.102

# Total robot width at wheel base, used for collision detection
# Note: the actual robot width is 13cm, but we add a litte bit of buffer
#       to faciliate sim-to-real transfer.
ROBOT_WIDTH = 0.13 + 0.02

# Note: the center of rotation (between the wheels) is not at the
#       geometric center see CAMERA_FORWARD_DIST
ROBOT_LENGTH = 0.18

# Height of the robot, used for scaling
ROBOT_HEIGHT = 0.12

# Safety radius multiplier
SAFETY_RAD_MULT = 1.8

# Robot safety circle radius
AGENT_SAFETY_RAD = (max(ROBOT_LENGTH, ROBOT_WIDTH) / 2) * SAFETY_RAD_MULT

# Minimum distance spawn position needs to be from all objects
MIN_SPAWN_OBJ_DIST = 0.25

# Road tile dimensions (2ft x 2ft, 61cm wide)
# self.road_tile_size = 0.61

# Maximum forward robot speed in meters/second
DEFAULT_ROBOT_SPEED = 1.20
# approx 2 tiles/second

DEFAULT_FRAMERATE = 30 

DEFAULT_MAX_STEPS = 1500

DEFAULT_MAP_NAME = "udem1"

DEFAULT_FRAME_SKIP = 1 

DEFAULT_ACCEPT_START_ANGLE_DEG = 60

REWARD_INVALID_POSE = -1000

MAX_SPAWN_ATTEMPTS = 10000

DEFAULT_SAFETY_FACTOR=1.0

DEFAULT_NUM_AGENTS=2

MAX_AGENTS=8


LanePosition0 = namedtuple("LanePosition", "dist dot_dir angle_deg angle_rad")


class LanePosition(LanePosition0):
    def as_json_dict(self):
        """Serialization-friendly format."""
        return dict(dist=self.dist, dot_dir=self.dot_dir, angle_deg=self.angle_deg, angle_rad=self.angle_rad)

   
class Simulator(gym.Env):
    """
    Simple road simulator to test RL training.
    Draws a road with turns using OpenGL, and simulates
    basic differential-drive dynamics.
    """

    metadata = {"render.modes": ["human", "rgb_array", "app"], "video.frames_per_second": 30}

    agents: List[Agent]
    cam_offset: np.ndarray
    road_tile_size: float
    grid_width: int
    grid_height: int
    timestamp: float
    state: str
    np_random: RandomState
    grid: List[TileDict]

    def __init__(
        self,
        safety_factor: float = DEFAULT_SAFETY_FACTOR,
        cam_mode: str = DEFAULT_CAM_MODE,
        map_name: str = DEFAULT_MAP_NAME,
        max_steps: int = DEFAULT_MAX_STEPS,
        draw_curve: bool = False,
        draw_bbox: bool = False,
        domain_rand: bool = True,
        frame_rate: float = DEFAULT_FRAMERATE,
        frame_skip: bool = DEFAULT_FRAME_SKIP,
        camera_width: int = DEFAULT_CAMERA_WIDTH,
        camera_height: int = DEFAULT_CAMERA_HEIGHT,
        robot_speed: float = DEFAULT_ROBOT_SPEED,
        robot_length: float = ROBOT_LENGTH,
        robot_width: float = ROBOT_WIDTH,
        accept_start_angle_deg=DEFAULT_ACCEPT_START_ANGLE_DEG,
        full_transparency: bool = False,
        seed: int = None,
        distortion: bool = False,
        dynamics_rand: bool = False,
        camera_rand: bool = False,
        randomize_maps_on_reset: bool = False,
        num_tris_distractors: int = 12,
        color_ground: Sequence[float] = (0.15, 0.15, 0.15),
        color_sky: Sequence[float] = BLUE_SKY,
        style: str = "photos",
        enable_leds: bool = True,
        num_agents: int = DEFAULT_NUM_AGENTS,
        num_random_agents: int = 0,
        max_agents: int = 0,
        verbose: bool = False 
    ):
        """

        :param duckie_bots:
        :param cam_mode:
        :param num_agents:
        :param num_random_agents:
        :param safety_factor:
        :param map_name:
        :param max_steps:
        :param draw_curve:
        :param draw_bbox:
        :param domain_rand: If true, applies domain randomization
        :param frame_rate:
        :param frame_skip:
        :param camera_width:
        :param camera_height:
        :param robot_speed: speed of ro
        :param accept_start_angle_deg:
        :param full_transparency:
        :param user_tile_start: If None, sample randomly. Otherwise (i,j). Overrides map start tile
        :param seed: Seed randomness
        :param state: If we are paused, running, or quit.
        :param distortion: If true, distorts the image with fish-eye approximation
        :param dynamics_rand: If true, perturbs the trim of the Duckiebot
        :param camera_rand: If true randomizes over camera miscalibration
        :param randomize_maps_on_reset: If true, randomizes the map on reset (Slows down training)
        :param style: String that represent which tiles will be loaded. One of ["photos", "synthetic"]
        :param enable_leds: Enables LEDs drawing.
        :param verbose: Enables Logging.
        """
        global MAX_AGENTS
        self.enable_leds = enable_leds
        information = get_graphics_information()
        logger.info(
            f"Information about the graphics card:",
            pyglet_version=pyglet.version,
            information=information,
            nvidia_around=os.path.exists("/proc/driver/nvidia/version"),
        )

        # first initialize the RNG
        self.seed_value = seed
        self.seed(seed=self.seed_value)
        self.num_tris_distractors = num_tris_distractors
        self.color_ground = color_ground
        self.color_sky = list(color_sky)

        # If true, then we publish all transparency information
        self.full_transparency = full_transparency

        # Map name, set in _load_map()
        self.map_name = None

        # Full map file path, set in _load_map()
        self.map_file_path = None

        # The parsed content of the map_file
        self.map_data = None

        # Maximum number of steps per episode
        self.max_steps = max_steps

        # Flag to draw the road curve
        self.draw_curve = draw_curve

        # Flag to draw bounding boxes
        self.draw_bbox = draw_bbox

        # Flag to enable/disable domain randomization
        self.domain_rand = domain_rand

        self.randomizer = Randomizer()

        # Frame rate to run at
        self.frame_rate = frame_rate
        self.delta_time = 1.0 / self.frame_rate

        # Number of frames to skip per action
        self.frame_skip = frame_skip

        # Produce graphical output
        self.graphics = True

        # Two-tuple of wheel torques, each in the range [-1, 1]
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        self.safety_factor = safety_factor 
        
        # Number of agents ( probably depricated)
        self.num_agents = num_agents 
        
        # Number of agents participating with random start
        self.num_random_agents = num_random_agents 
        
        # Camera settings
        self.cam_mode = cam_mode 
        self.camera_width = camera_width
        self.camera_height = camera_height

        # Default robot information
        self.robot_speed = robot_speed
        self.robot_length = robot_length
        self.robot_width = robot_width
        
        # We observe an RGB image with pixels in [0, 255]
        # Note: the pixels are in uint8 format because this is more compact
        # than float32 if sent over the network or stored in a dataset
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.camera_height, self.camera_width, 3), dtype=np.uint8
        )

        self.reward_range = (-1000, 1000)

        # Window for displaying the environment to humans
        self.window = None
        self.text_window = None

        # Invisible window to render into (shadow OpenGL context)
        self.shadow_window = pyglet.window.Window(width=1, height=1, visible=False)

        # For displaying text
        self.text_label = pyglet.text.Label(font_name="Arial", font_size=14, x=5, y=WINDOW_HEIGHT - 19)

        # Create a frame buffer object for the observation
        self.multi_fbo, self.final_fbo = create_frame_buffers(self.camera_width, self.camera_height, 4)

        # Array to render the image into (for observation rendering)
        self.img_array = np.zeros(shape=self.observation_space.shape, dtype=np.uint8)

        # Create a frame buffer object for human rendering
        self.multi_fbo_human, self.final_fbo_human = create_frame_buffers(WINDOW_WIDTH, WINDOW_HEIGHT, 4)

        # Array to render the image into (for human rendering)
        self.img_array_human = np.zeros(shape=(WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

        # allowed angle in lane for starting position
        self.accept_start_angle_deg = accept_start_angle_deg

        # Initialize Agents
        self.agents = []

        # Load the map
        self._load_map(map_name)

        # Distortion params, if so, load the library, only if not bbox mode
        self.distortion = distortion and not draw_bbox
        self.camera_rand = False
        if not draw_bbox and distortion:
            if distortion:
                self.camera_rand = camera_rand

                self.camera_model = Distortion(camera_rand=self.camera_rand)

        # Used by the UndistortWrapper, always initialized to False
        self.undistort = False

        # Dynamics randomization
        self.dynamics_rand = dynamics_rand

        self.style = style

        self.randomize_maps_on_reset = randomize_maps_on_reset

        if self.randomize_maps_on_reset:
            self.map_names = os.listdir(get_subdir_path("maps"))
            self.map_names = [
                _map for _map in self.map_names if not _map.startswith(("calibration", "regress"))
            ]
            self.map_names = [mapfile.replace(".yaml", "") for mapfile in self.map_names]

        # Logging
        self.verbose = verbose

        # Set the default state to running
        self.state = "run"
        self.max_agents = max_agents
        MAX_AGENTS = max_agents
        self.c_info_struct = None


        # Initialize the state
        self.reset()


    def _init_vlists(self):
        ns = 8
        assert ns >= 2

        # half_size = self.road_tile_size / 2
        TS = self.road_tile_size

        def get_point(u, v):
            pu = u / (ns - 1)
            pv = v / (ns - 1)
            x = -TS / 2 + pu * TS
            z = -TS / 2 + pv * TS
            tu = pu
            tv = 1 - pv
            return (x, 0.0, z), (tu, tv)

        vertices = []
        textures = []
        normals = []
        colors = []
        for i, j in itertools.product(range(ns - 1), range(ns - 1)):
            tl_p, tl_t = get_point(i, j)
            tr_p, tr_t = get_point(i + 1, j)
            br_p, br_t = get_point(i, j + 1)
            bl_p, bl_t = get_point(i + 1, j + 1)
            normal = [0.0, 1.0, 0.0]

            color = (255, 255, 255, 255)
            vertices.extend(tl_p)
            textures.extend(tl_t)
            normals.extend(normal)
            colors.extend(color)

            vertices.extend(tr_p)
            textures.extend(tr_t)
            normals.extend(normal)
            colors.extend(color)

            vertices.extend(bl_p)
            textures.extend(bl_t)
            normals.extend(normal)
            colors.extend(color)

            vertices.extend(br_p)
            textures.extend(br_t)
            normals.extend(normal)
            colors.extend(color)

        total = len(vertices) // 3
        self.road_vlist = pyglet.graphics.vertex_list(
            total, ("v3f", vertices), ("t2f", textures), ("n3f", normals), ("c4B", colors)
        )
        logger.info("done")
        # Create the vertex list for the ground quad
        verts = [
            -1,
            -0.8,
            1,
            #
            -1,
            -0.8,
            -1,
            #
            1,
            -0.8,
            -1,  #
            1,
            -0.8,
            1,
        ]
        self.ground_vlist = pyglet.graphics.vertex_list(4, ("v3f", verts))

    # Store state in dictionary to access later without recomputing
    def get_agents_states(self):
        env = self
        radius = (env.road_tile_size)
        for agent in self.agents: 
            agent.states['in_intersection'] = agent.in_intersection(env)
        for agent in self.agents: 
            agent.states['at_intersection_entry'] = agent.at_intersection_entry(env)
        for agent in self.agents: 
            agent.states['intersection_empty'] = agent.intersection_empty(env)
        for agent in self.agents: 
            agent.states['approaching_intersection'] = agent.approaching_intersection(env)
        for agent in self.agents: 
            agent.states['obj_in_range'] = agent.object_in_range(env, location="Ahead", radius = radius)
        for agent in self.agents: 
            agent.states['has_right_of_way'] = agent.has_right_of_way(env)
        for agent in self.agents: 
            agent.states['next_to_go'] = agent.next_to_go(env)
        for agent in self.agents: 
            agent.states['safe_to_enter'] = agent.safe_to_enter(env)
        for agent in self.agents: 
            agent.states['cars_waiting_to_enter'] = agent.cars_waiting_to_enter(env)
        for agent in self.agents: 
            agent.states['car_entering_range'] = agent.car_entering_range(env, radius=radius)
        for agent in self.agents: 
            agent.states['obj_behind_intersection'] = agent.object_in_range(env, location="Behind", intersection=True, radius=radius)
        for agent in self.agents: 
            agent.states['obj_behind_no_intersection'] =  agent.object_in_range(env, location="Behind", intersection=False, radius=radius)
        for agent in self.agents: 
            agent.states['is_tailgating'] =  agent.is_tailgating(env)
    
    def reset(self, segment: bool = False, webserver_reset: bool = False):
        """
        Reset the simulation at the start of a new episode
        This also randomizes many environment parameters (domain randomization)
        """

        if self.window:
            self.window.clear()
            self.text_window.clear()
            self.close()
        
        # Step count since episode start
        self.timestamp = 0.0

        # Get the random number of agents from 
        if not webserver_reset:
            self.agents = []
            random_agents = self.np_random.integers(0, self.num_random_agents)
            self._load_agents(self.map_data, random_agents=random_agents, webserver_reset=webserver_reset)

        # Reset each agent
        for agent in self.agents:
            agent.speed = 0.0
            agent.index = int(agent.agent_id[-1])
            agent.step_count = 0
            agent.actions = []
            agent.nearby_objects = []
            agent.nearby_agents = []
            agent.timestamp = 0.0
            agent.last_action = None
            agent.wheelVels = np.array([0.0, 0.0]) 
            agent.state = None
            agent.intersection_arrival = -1
            agent.lights["front_left"][3] = False
            agent.lights["front_right"][3] = False
            agent.lights["back_left"][3] = False
            agent.lights["back_right"][3] = False
            agent.lights["center"][3] = False
            agent.patience = 0
            agent.direction = agent.get_direction(self)
            agent.states['in_intersection'] = False
            agent.states['at_intersection_entry'] = False
            agent.states['intersection_empty'] = False
            agent.states['approaching_intersection'] = False
            agent.states['obj_in_range'] = False
            agent.states['has_right_of_way'] = False
            agent.states['cars_waiting_to_enter'] = False
            agent.states['car_entering_range'] = False
            agent.states['obj_behind_intersection'] = False
            agent.states['obj_behind_no_intersection'] = False
            agent.states['is_tailgating'] = False
            agent.states['next_to_go'] = False
        
                    

        if self.randomize_maps_on_reset:
            map_name = self.np_random.choice(self.map_names)
            logger.info(f"Random map chosen: {map_name}")
            self._load_map(map_name)

        self.randomization_settings = self.randomizer.randomize(rng=self.np_random)

        # Horizon color
        # Note: we explicitly sample white and grey/black because
        # these colors are easily confused for road and lane markings
        if self.domain_rand:
            horz_mode = self.randomization_settings["horz_mode"]
            if horz_mode == 0:
                self.horizon_color = self._perturb(self.color_sky)
            elif horz_mode == 1:
                self.horizon_color = self._perturb(WALL_COLOR)
            elif horz_mode == 2:
                self.horizon_color = self._perturb([0.15, 0.15, 0.15], 0.4)
            elif horz_mode == 3:
                self.horizon_color = self._perturb([0.9, 0.9, 0.9], 0.4)
        else:
            self.horizon_color = self.color_sky

        # Setup some basic lighting with a far away sun
        if self.domain_rand:
            light_pos = self.randomization_settings["light_pos"]
        else:
            #light_pos = [-40, 200, 100, 0.0]
            light_pos = [0.0, 3.0, 0.0, 1.0]

        # Lighting Initialization
        DIM = 1.0
        ambient = np.array([0.50 * DIM, 0.50 * DIM, 0.50 * DIM, 1])
        ambient = self._perturb(ambient, 0.3)
        diffuse = np.array([0.70 * DIM, 0.70 * DIM, 0.70 * DIM, 1])
        diffuse = self._perturb(diffuse, 0.99)
        specular = np.array([0.0, 0.0, 0.0, 1])

        # Light drawing
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, (gl.GLfloat * 4)(*light_pos))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, (gl.GLfloat * 4)(*ambient))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, (gl.GLfloat * 4)(*diffuse))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, (gl.GLfloat * 4)(*specular))

        # Reset lighting
        gl.glDisable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_LIGHTING)
        
        gl.glEnable(gl.GL_COLOR_MATERIAL)

        # Ground color
        self.ground_color = self._perturb(np.array(self.color_ground), 0.3)

        # Distance between the robot's wheels
        self.wheel_dist = self._perturb(WHEEL_DIST)

        # Distance bewteen camera and ground
        self.cam_height = CAMERA_FLOOR_DIST

        # Angle at which the camera is rotated
        self.cam_angle = [CAMERA_ANGLE, 0, 0]

        # Field of view angle of the camera
        self.cam_fov_y = CAMERA_FOV_Y

        # Perturb using randomization API (either if domain rand or only camera rand
        if self.domain_rand or self.camera_rand:
            self.cam_height *= self.randomization_settings["camera_height"]
            self.cam_angle = [CAMERA_ANGLE * self.randomization_settings["camera_angle"], 0, 0]
            self.cam_fov_y *= self.randomization_settings["camera_fov_y"]

        # Camera offset for use in free camera mode
        self.cam_offset = np.array([0, 0, 0])

        # Create the vertex list for the ground/noise triangles
        # These are distractors, junk on the floor
        numTris = self.num_tris_distractors
        verts = []
        colors = []
        for _ in range(0, 3 * numTris):
            p = self.np_random.uniform(low=[-20, -0.6, -20], high=[20, -0.3, 20], size=(3,))
            c = self.np_random.uniform(low=0, high=0.9)
            c = self._perturb([c, c, c], 0.1)
            verts += [p[0], p[1], p[2]]
            colors += [c[0], c[1], c[2]]

        self.tri_vlist = pyglet.graphics.vertex_list(3 * numTris, ("v3f", verts), ("c3f", colors))

        # Randomize tile parameters
        for tile in self.grid:
            rng = self.np_random if self.domain_rand else None

            kind = tile["kind"]
            fn = get_texture_file(f"tiles-processed/{self.style}/{kind}/texture")[0]
            t = load_texture(fn, segment=False, segment_into_color=False)
            tt = Texture(t, tex_name=kind, rng=rng)
            tile["texture"] = tt

            # Random tile color multiplier
            tile["color"] = self._perturb([1, 1, 1, 1], 0.2)

        # Randomize object parameters
        for obj in self.objects:
            # Randomize the object color
            obj.color = self._perturb([1, 1, 1, 1], 0.3)

            # Randomize whether the object is visible or not
            if obj.optional and self.domain_rand:
                obj.visible = self.np_random.randint(0, 2) == 0
            else:
                obj.visible = True

        # Spawn agents
        directions = ['N', 'N',  'S', 'S', 'E', 'E', 'W', 'W']
        colors = ['green', 'red', 'grey', 'cyan', 'yellow', 'orange', 'midnight']
        for agent in self.agents: 
            # If random spawn
            if agent.random_spawn and not webserver_reset:
                self.spawn_random_agent(agent, directions, colors)
            # If the map specifies a starting tile
            elif agent.start_tile and not agent.random_spawn:
                tile = self._get_tile(agent.start_tile[0], agent.start_tile[1])
            else:
                # Select a random drivable tile to start on
                if not self.drivable_tiles:
                    msg = "There are no drivable tiles. Use start_tile or agent.start_tile"
                    raise Exception(msg)
                tile_idx = self.np_random.integers(0, len(self.drivable_tiles))
                tile = self.drivable_tiles[tile_idx]

            # If setting from the webserver, use that information for propose angle and position
            if webserver_reset:
                propose_pos = agent.cur_pos 
                print("HERE")
                print(f"Agent current pos{agent.cur_pos}")
                propose_angle = agent.cur_angle

            # If specified from map, use that information
            elif agent.start_pose and not agent.random_spawn:
                if self.verbose:
                    logger.info(f"using map pose start for agent {agent.agent_id}: {agent.start_pose}")

                i, j = tile["coords"]
                x = i * self.road_tile_size + agent.start_pose[0][0]
                z = j * self.road_tile_size + agent.start_pose[0][2]
                propose_pos = np.array([x, 0, z])
                propose_angle = agent.start_pose[1]

                if self.verbose:
                    logger.info(f"Using map pose start for agent {agent.agent_id}. \n Pose: {propose_pos}, Angle: {propose_angle}")

            # If its not a good random spawn, find a valid point.
            elif not agent.random_spawn:
                # Keep trying to find a valid spawn position on this tile
                for _ in range(MAX_SPAWN_ATTEMPTS):
                    i, j = tile["coords"]

                    # Choose a random position on this tile
                    x = self.np_random.uniform(i, i + 1) * self.road_tile_size
                    z = self.np_random.uniform(j, j + 1) * self.road_tile_size
                    propose_pos = np.array([x, 0, z])

                    # Choose a random direction
                    propose_angle = self.np_random.uniform(0, 2 * math.pi)

                    # logger.debug('Sampled %s %s angle %s' % (propose_pos[0],
                    #                                          propose_pos[1],
                    #                                          np.rad2deg(propose_angle)))

                    # If this is too close to an object or not a valid pose, retry
                    inconvenient = self._inconvenient_spawn(propose_pos)

                    if inconvenient:
                        # msg = 'The spawn was inconvenient.'
                        # logger.warning(msg)
                        continue

                    invalid = not self._valid_pose(propose_pos, propose_angle, agent, safety_factor=1.3)
                    if invalid:
                        # msg = 'The spawn was invalid.'
                        # logger.warning(msg)
                        continue

                    # If the angle is too far away from the driving direction, retry
                    try:
                        lp = self.get_lane_pos2(propose_pos, propose_angle)
                    except NotInLane:
                        continue
                    M = self.accept_start_angle_deg
                    ok = -M < lp.angle_deg < +M
                    if not ok:
                        continue
                    # Found a valid initial pose
                    break
                else:
                    msg = f"Could not find a valid starting pose after {MAX_SPAWN_ATTEMPTS} attempts"
                    logger.warn(msg)
                    propose_pos = np.array([1, 0, 1])
                    propose_angle = 1

                    # raise Exception(msg)

            ### ABOVE ONLY GETS PROPOSE POS AND ANGLE. NEED TO DO THE REST HERE
            if (not agent.random_spawn) or webserver_reset:
                agent.cur_pos = propose_pos
                agent.prev_pos = propose_pos
                agent.cur_angle = propose_angle

                init_vel = np.array([0, 0])

                # Initialize Dynamics model
                if self.dynamics_rand:
                    trim = 0 + self.randomization_settings["trim"][0]
                    p = get_DB18_uncalibrated(delay=0.15, trim=trim)
                else:
                    p = get_DB18_nominal(delay=0.15)

                q = self.cartesian_from_weird(agent.cur_pos, agent.cur_angle)
                v0 = geometry.se2_from_linear_angular(init_vel, 0)
                c0 = q, v0
                agent.state = p.initialize(c0=c0, t0=0)

                logger.info(f"Starting agent {agent.agent_id} at:\nPosition:{agent.cur_pos} {agent.cur_angle}\nForward Step: {agent.forward_step}\nTurn Choice:{agent.turn_choice}\nSignal Choice:{agent.signal_choice}\nActions:{agent.actions}\nSpeed:{agent.speed}\nState:{agent.state}")

            # set the curve
            agent.curve = agent.get_curve(self)
            agent.direction = agent.get_direction(self)
            agent.initial_direction = agent.get_direction(self)
        

        # Generate the first camera image
        #obs = self.render_obs(segment=segment)
        self.c_info_struct = EnvironmentInfo(self)
        self.get_agents_states()


        # Return first observation
        return #obs

    def _load_map(self, map_name: str):
        """
        Load the map layout from a YAML file
        """

        map_name = "maps/" + map_name
        # Store the map name
        if os.path.exists(map_name) and os.path.isfile(map_name):
            # if env is loaded using gym's register function, we need to extract the map name from the complete url
            #map_name = os.path.basename(map_name)
            assert map_name.endswith(".yaml")
            map_name = ".".join(map_name.split(".")[:-1])
        self.map_name = map_name

        # Get the full map file path
        self.map_file_path = get_resource_path(f"{map_name}.yaml")

        logger.debug(f'loading map file "{self.map_file_path}"')

        with open(self.map_file_path, "r") as f:
            self.map_data = yaml.load(f, Loader=yaml.Loader)

        self._interpret_map(self.map_data)

    # Read in and initialize values from the map
    def _interpret_map(self, map_data: MapFormat1):
        try:
            if not "tile_size" in map_data:
                msg = "Must now include explicit tile_size in the map data."
                raise InvalidMapException(msg)
            self.road_tile_size = map_data["tile_size"]
            self._init_vlists()

            tiles = map_data["tiles"]
            assert len(tiles) > 0
            assert len(tiles[0]) > 0

            # Create the grid
            self.grid_height = len(tiles)
            self.grid_width = len(tiles[0])
            # noinspection PyTypeChecker
            self.grid = [None] * self.grid_width * self.grid_height

            # We keep a separate list of drivable tiles
            self.drivable_tiles = []

            # For each row in the grid
            for j, row in enumerate(tiles):

                if len(row) != self.grid_width:
                    msg = "each row of tiles must have the same length"
                    raise InvalidMapException(msg, row=row)

                # For each tile in this row
                for i, tile in enumerate(row):
                    tile = tile.strip()

                    if tile == "empty":
                        continue

                    directions = ["S", "E", "N", "W"]
                    default_orient = "E"

                    if "/" in tile:
                        kind, orient = tile.split("/")
                        kind = kind.strip(" ")
                        orient = orient.strip(" ")
                        angle = directions.index(orient)

                    elif "4" in tile:
                        kind = "4way"
                        angle = directions.index(default_orient)

                    else:
                        kind = tile
                        angle = directions.index(default_orient)

                    DRIVABLE_TILES = [
                        "straight",
                        "curve_left",
                        "curve_right",
                        "3way_left",
                        "3way_right",
                        "4way",
                    ]
                    drivable = kind in DRIVABLE_TILES

                    # logger.info(f'kind {kind} drivable {drivable} row = {row}')

                    tile = cast(
                        TileDict, {"coords": (i, j), "kind": kind, "angle": angle, "drivable": drivable}
                    )

                    self._set_tile(i, j, tile)

                    if drivable:
                        tile["curves"] = self._get_curve(i, j)
                        self.drivable_tiles.append(tile)

            # Load objects and agents from map data
            self._load_objects(map_data)
            self._load_agents(map_data)

        except Exception as e:
            msg = "Cannot load map data"
            print(e)
            raise InvalidMapException(msg, map_data=map_data)

    # Load each of the agents from the map
    def _load_agents(self, map_data: MapFormat1, random_agents: int = None, webserver_reset: bool = False):
        agents = []
        try:
            agents = map_data["agents"]
        except KeyError:
            pass

        if agents:
            # If reading in from map
            for agent_id, desc in agents.items():
                new_agent = Agent(self, cur_pos=desc["start_pose"][0], cur_angle=desc["start_pose"][1], start_tile=desc["start_tile"], start_pose=desc["start_pose"], agent_id=agent_id, color=desc["color"])
                self.agents.append(new_agent)
        else:
            # Retroactive Support
            try: 
                if map_data["start_pose"] and map_data["start_tile"]:
                    new_agent = Agent(self, cur_pos=map_data["start_pose"][0], cur_angle=map_data["start_pose"][1], start_tile=map_data["start_tile"], start_pose=map_data["start_pose"], agent_id="agent0")
                    self.agents.append(new_agent)
                elif map_data["start_pose"]:
                    new_agent = Agent(self, cur_pos=map_data["start_pose"][0], cur_angle=map_data["start_pose"][1], start_pose=map_data["start_pose"], agent_id="agent0")
                    self.agents.append(new_agent)
                elif map_data["start_tile"]:
                    new_agent = Agent(self, start_tile=desc["start_tile"], agent_id="agent0")
                    self.agents.append(new_agent)
            except KeyError:
                pass
           
        # If we have none, init all as good random ones
        if not self.agents:
            num_random = self.num_random_agents
            if random_agents:
                num_random = random_agents
            for x in range(0, num_random):
                new_agent = Agent(self, cur_pos=[0, 0, 0], cur_angle=0, agent_id=("agent" + str(x)), random_spawn=True)
                self.agents.append(new_agent)


        # If still no, make a default one ( no random agents )
        if not self.agents:
            print("HERE strange.")
            new_agenv = Agent(self, cur_pos=[0, 0, 0], cur_angle=0, agent_id="agent" + str(x), random_spawn=True)
        

    def _load_objects(self, map_data: MapFormat1):
        # Create the objects array
        self.objects = []

        # The corners for every object, regardless if collidable or not
        self.object_corners = []

        # Arrays for checking collisions with N static objects
        # (Dynamic objects done separately)
        # (N x 2): Object position used in calculating reward
        self.collidable_centers = []

        # (N x 2 x 4): 4 corners - (x, z) - for object's boundbox
        self.collidable_corners = []

        # (N x 2 x 2): two 2D norms for each object (1 per axis of boundbox)
        self.collidable_norms = []

        # (N): Safety radius for object used in calculating reward
        self.collidable_safety_radii = []

        # For each object
        try:
            objects = map_data["objects"]
        except KeyError:
            pass
        else:
            if isinstance(objects, list):
                for obj_idx, desc in enumerate(objects):
                    kind = desc["kind"]
                    obj_name = f"ob{obj_idx:02d}-{kind}"
                    self.interpret_object(obj_name, desc)
            elif isinstance(objects, dict):
                for obj_name, desc in objects.items():
                    self.interpret_object(obj_name, desc)
            else:
                raise ValueError(objects)

        # If there are collidable objects
        if len(self.collidable_corners) > 0:
            self.collidable_corners = np.stack(self.collidable_corners, axis=0)
            self.collidable_norms = np.stack(self.collidable_norms, axis=0)

            # Stack doesn't do anything if there's only one object,
            # So we add an extra dimension to avoid shape errors later
            if len(self.collidable_corners.shape) == 2:
                self.collidable_corners = self.collidable_corners[np.newaxis]
                self.collidable_norms = self.collidable_norms[np.newaxis]

        self.collidable_centers = np.array(self.collidable_centers)
        self.collidable_safety_radii = np.array(self.collidable_safety_radii)

    # Initialize and read from the map
    def interpret_object(self, objname: str, desc: MapFormat1Object):
        kind = desc["kind"]
        name = desc.get("name", objname)
        actions = []

        W = self.grid_width
        tile_size = self.road_tile_size
        transform: SE2Transform = get_transform(desc, W, tile_size)
        # logger.info(desc=desc, transform=transform)

        pose = transform.as_SE2()

        pos, angle_rad = self.weird_from_cartesian(pose)

        optional = desc.get("optional", False)

        # Load the mesh
        if kind == MapFormat1Constants.KIND_DUCKIEBOT:
            use_color = desc.get("color", "red")
            mesh = get_duckiebot_mesh(use_color)
        elif kind.startswith("sign"):
            change_materials: Dict[str, MatInfo]
            # logger.info(kind=kind, desc=desc)
            minfo = cast(MatInfo, {"map_Kd": f"{kind}.png"})
            change_materials = {"April_Tag": minfo}
            mesh = get_mesh("sign_generic", change_materials=change_materials)
        elif kind == "floor_tag":
            return
        else:
            mesh = get_mesh(kind)

        # Scale mesh
        if "height" in desc:
            scale = desc["height"] / mesh.max_coords[1]
        else:
            if "scale" in desc:
                scale = desc["scale"]
            else:
                scale = 1.0
        assert not ("height" in desc and "scale" in desc), "cannot specify both height and scale"

        static = desc.get("static", True)
        agent = desc.get("agent", False)

        # Descriptions of objects
        obj_desc = {
            "kind": kind,
            "mesh": mesh,
            "pos": pos,
            "angle": angle_rad,
            "scale": scale,
            "optional": optional,
            "static": static,
            "agent": agent,
            "name": name,
            "actions": actions,
        }

        if static:
            if kind == MF1C.KIND_TRAFFICLIGHT:
                obj = TrafficLightObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT)
            else:
                obj = WorldObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT)
        else:
            if kind == MF1C.KIND_DUCKIEBOT:
                obj = DuckiebotObj(
                    obj_desc, self.domain_rand, SAFETY_RAD_MULT, WHEEL_DIST, ROBOT_WIDTH, ROBOT_LENGTH
                )
            elif kind == MF1C.KIND_DUCKIE:
                obj = DuckieObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT, self.road_tile_size)
            elif kind == MF1C.KIND_CHECKERBOARD:
                obj = CheckerboardObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT, self.road_tile_size)
            else:
                msg = "Object kind unknown."
                raise InvalidMapException(msg, kind=kind)

        self.objects.append(obj)

        # If the object intersects with a drivable tile
        if (
            static
            and kind != MF1C.KIND_TRAFFICLIGHT
            # We want collision checking also for things outside the lanes
        ):
            # noinspection PyUnresolvedReferences
            self.collidable_centers.append(pos)  # XXX: changes types during initialization
            self.collidable_corners.append(obj.obj_corners.T)
            self.collidable_norms.append(obj.obj_norm)
            # noinspection PyUnresolvedReferences
            self.collidable_safety_radii.append(obj.safety_radius)  # XXX: changes types during initialization

    def close(self):
        pass

    # Set seed
    def seed(self, seed=None):
        self.np_random, _ = seeding.np_random(seed)
        return [seed]

    # Change a tile
    def _set_tile(self, i: int, j: int, tile: TileDict) -> None:
        assert 0 <= i < self.grid_width
        assert 0 <= j < self.grid_height
        index: int = j * self.grid_width + i
        self.grid[index] = tile

    # Return a tile
    def _get_tile(self, i: int, j: int) -> Optional[TileDict]:
        """
        Returns None if the duckiebot is not in a tile.
        """
        i = int(i)
        j = int(j)
        if i < 0 or i >= self.grid_width:
            return None
        if j < 0 or j >= self.grid_height:
            return None
        return self.grid[j * self.grid_width + i]

    def _perturb(self, val: Union[float, np.ndarray, List[float]], scale: float = 0.1) -> np.ndarray:
        """
        Add noise to a value. This is used for domain randomization.
        """
        assert 0 <= scale < 1

        val = np.array(val)

        if not self.domain_rand:
            return val

        if isinstance(val, np.ndarray):
            noise = self.np_random.uniform(low=1 - scale, high=1 + scale, size=val.shape)
            if val.size == 4:
                noise[3] = 1
        else:
            noise = self.np_random.uniform(low=1 - scale, high=1 + scale)

        res = val * noise

        return res

    # Check if objects collide
    def _collidable_object(self, obj_corners, obj_norm, possible_tiles):
        """
        A function to check if an object intersects with any
        drivable tiles, which would mean our agent could run into them.
        Helps optimize collision checking with agent during runtime
        """

        if possible_tiles.shape == 0:
            return False

        drivable_tiles = []
        for c in possible_tiles:
            tile = self._get_tile(c[0], c[1])
            if tile and tile["drivable"]:
                drivable_tiles.append((c[0], c[1]))

        if not drivable_tiles:
            return False

        drivable_tiles = np.array(drivable_tiles)

        # Tiles are axis aligned, so add normal vectors in bulk
        tile_norms = np.array([[1, 0], [0, 1]] * len(drivable_tiles))

        # None of the candidate tiles are drivable, don't add object
        if len(drivable_tiles) == 0:
            return False

        # Find the corners for each candidate tile
        drivable_tiles = np.array(
            [
                tile_corners(self._get_tile(pt[0], pt[1])["coords"], self.road_tile_size).T
                for pt in drivable_tiles
            ]
        )

        # Stack doesn't do anything if there's only one object,
        # So we add an extra dimension to avoid shape errors later
        if len(tile_norms.shape) == 2:
            tile_norms = tile_norms[np.newaxis]
        else:  # Stack works as expected
            drivable_tiles = np.stack(drivable_tiles, axis=0)
            tile_norms = np.stack(tile_norms, axis=0)

        # Only add it if one of the vertices is on a drivable tile
        return intersects(obj_corners, drivable_tiles, obj_norm, tile_norms)

    # Compute the grid coordinates from a position
    def get_grid_coords(self, abs_pos: np.array) -> Tuple[int, int]:
        """
        Compute the tile indices (i,j) for a given (x,_,z) world position

        x-axis maps to increasing i indices
        z-axis maps to increasing j indices

        Note: may return coordinates outside of the grid if the
        position entered is outside of the grid.
        """

        x, _, z = abs_pos
        i = math.floor(x / self.road_tile_size)
        j = math.floor(z / self.road_tile_size)

        return int(i), int(j)

    # Get the curve points on a tile
    def _get_curve(self, i, j):
        """
        Get the Bezier curve control points for a given tile
        """
        tile = self._get_tile(i, j)
        assert tile is not None

        kind = tile["kind"]
        angle = tile["angle"]

        # Each tile will have a unique set of control points,
        # Corresponding to each of its possible turns
        if kind.startswith("straight"):
            pts = (
                np.array(
                    [
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, -0.25],
                            [-0.20, 0, 0.25],
                            [-0.20, 0, 0.50],
                        ],
                        [
                            [0.20, 0, 0.50],
                            [0.20, 0, 0.25],
                            [0.20, 0, -0.25],
                            [0.20, 0, -0.50],
                        ],
                    ]
                )
                * self.road_tile_size
            )
        elif kind == "curve_left":
            pts = (
                np.array(
                    [
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, 0.00],
                            [0.00, 0, 0.20],
                            [0.50, 0, 0.20],
                        ],
                        [
                            [0.50, 0, -0.20],
                            [0.30, 0, -0.20],
                            [0.20, 0, -0.30],
                            [0.20, 0, -0.50],
                        ],
                    ]
                )
                * self.road_tile_size
            )
        elif kind == "curve_right":
            pts = (
                np.array(
                    [
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, -0.20],
                            [-0.30, 0, -0.20],
                            [-0.50, 0, -0.20],
                        ],
                        [
                            [-0.50, 0, 0.20],
                            [-0.30, 0, 0.20],
                            [0.30, 0, 0.00],
                            [0.20, 0, -0.50],
                        ],
                    ]
                )
                * self.road_tile_size
            )
        # Hardcoded all curves for 3way intersection
        elif kind.startswith("3way"):
            pts = (
                np.array(
                    [
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, -0.25],
                            [-0.20, 0, 0.25],
                            [-0.20, 0, 0.50],
                        ],
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, 0.00],
                            [0.00, 0, 0.20],
                            [0.50, 0, 0.20],
                        ],
                        [
                            [0.20, 0, 0.50],
                            [0.20, 0, 0.25],
                            [0.20, 0, -0.25],
                            [0.20, 0, -0.50],
                        ],
                        [
                            [0.50, 0, -0.20],
                            [0.30, 0, -0.20],
                            [0.20, 0, -0.20],
                            [0.20, 0, -0.50],
                        ],
                        [
                            [0.20, 0, 0.50],
                            [0.20, 0, 0.20],
                            [0.30, 0, 0.20],
                            [0.50, 0, 0.20],
                        ],
                        [
                            [0.50, 0, -0.20],
                            [0.30, 0, -0.20],
                            [-0.20, 0, 0.00],
                            [-0.20, 0, 0.50],
                        ],
                    ]
                )
                * self.road_tile_size
            )

        # Template for each side of 4way intersection
        elif kind.startswith("4way"):
            pts = (
                np.array(
                    [
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, 0.00],
                            [0.00, 0, 0.20],
                            [0.50, 0, 0.20],
                        ],
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, -0.25],
                            [-0.20, 0, 0.25],
                            [-0.20, 0, 0.50],
                        ],
                        [
                            [-0.20, 0, -0.50],
                            [-0.20, 0, -0.20],
                            [-0.30, 0, -0.20],
                            [-0.50, 0, -0.20],
                        ],
                    ]
                )
                * self.road_tile_size
            )
        else:
            msg = "Cannot get bezier for kind"
            raise InvalidMapException(msg, kind=kind)

        # Rotate and align each curve with its place in global frame
        if kind.startswith("4way"):
            fourway_pts = []
            # Generate all four sides' curves,
            # with 3-points template above
            for rot in np.arange(0, 4):
                mat = gen_rot_matrix(np.array([0, 1, 0]), rot * math.pi / 2)
                pts_new = np.matmul(pts, mat)
                pts_new += np.array([(i + 0.5) * self.road_tile_size, 0, (j + 0.5) * self.road_tile_size])
                fourway_pts.append(pts_new)

            fourway_pts = np.reshape(np.array(fourway_pts), (12, 4, 3))
            return fourway_pts

        # Hardcoded each curve; just rotate and shift
        elif kind.startswith("3way"):
            threeway_pts = []
            mat = gen_rot_matrix(np.array([0, 1, 0]), angle * math.pi / 2)
            pts_new = np.matmul(pts, mat)
            pts_new += np.array([(i + 0.5) * self.road_tile_size, 0, (j + 0.5) * self.road_tile_size])
            threeway_pts.append(pts_new)

            threeway_pts = np.array(threeway_pts)
            threeway_pts = np.reshape(threeway_pts, (6, 4, 3))
            return threeway_pts

        else:
            mat = gen_rot_matrix(np.array([0, 1, 0]), angle * math.pi / 2)
            pts = np.matmul(pts, mat)
            pts += np.array([(i + 0.5) * self.road_tile_size, 0, (j + 0.5) * self.road_tile_size])

        return pts

    # Find the closest curve point
    def closest_curve_point(
        self, pos: np.array, angle: float, index=None) -> Tuple[Optional[np.array], Optional[np.array]]:
        """
        Get the closest point on the curve to a given point
        Also returns the tangent at that point.

        Returns None, None if not in a lane.
        """

        i, j = self.get_grid_coords(pos)
        tile = self._get_tile(i, j)

        if tile is None or not tile["drivable"]:
            return None, None

        # Find curve with largest dotproduct with heading
        curves = self._get_tile(i, j)["curves"]

        curve_headings = curves[:, -1, :] - curves[:, 0, :]
        curve_headings = curve_headings / np.linalg.norm(curve_headings).reshape(1, -1)
        
        dir_vec = get_dir_vec(angle)

        dot_prods = np.dot(curve_headings, dir_vec)
        cps = curves[np.argmax(dot_prods)]

        if index != None:
            cps = curves[index]

        # Find closest point and tangent to this curve
        t = bezier_closest(cps, pos)
        point = bezier_point(cps, t)
        tangent = bezier_tangent(cps, t)

        return point, tangent

    def get_lane_pos2(self, pos, angle, index=None, curve_point=None, curve_tangent=None):
        """
        Get the position of the agent relative to the center of the right lane

        Raises NotInLane if the Duckiebot is not in a lane.
        """

        # Get the closest point along the right lane's Bezier curve,
        # and the tangent at that point
        if curve_point and curve_tangent:
            point = np.array(curve_point)
            tangent = np.array(curve_tangent)
        else:
            point, tangent = self.closest_curve_point(pos, angle, index=index)
        if point is None or tangent is None:
            msg = f"Point not in lane: {pos}"
            raise NotInLane(msg)

        assert point is not None and tangent is not None

        # Compute the alignment of the agent direction with the curve tangent
        dirVec = get_dir_vec(angle)
        dotDir = np.dot(dirVec, tangent)
        dotDir = np.clip(dotDir, -1.0, +1.0)

        # Compute the signed distance to the curve
        # Right of the curve is negative, left is positive
        posVec = pos - point
        upVec = np.array([0, 1, 0])
        rightVec = np.cross(tangent, upVec)
        signedDist = np.dot(posVec, rightVec)

        # Compute the signed angle between the direction and curve tangent
        # Right of the tangent is negative, left is positive
        angle_rad = math.acos(dotDir)

        if np.dot(dirVec, rightVec) < 0:
            angle_rad *= -1

        angle_deg = np.rad2deg(angle_rad)
        # return signedDist, dotDir, angle_deg

        return LanePosition(dist=signedDist, dot_dir=dotDir, angle_deg=angle_deg, angle_rad=angle_rad)

    def _drivable_pos(self, pos) -> bool:
        """
        Check that the given (x,y,z) position is on a drivable tile
        """

        coords = self.get_grid_coords(pos)
        tile = self._get_tile(*coords)
        if tile is None:
            msg = f"No tile found at {pos} {coords}"
            if self.verbose:
                logger.debug(msg)
            return False

        if not tile["drivable"]:
            msg = f"{pos} corresponds to tile at {coords} which is not drivable: {tile}"
            if self.verbose:
                logger.debug(msg)
            return False

        return True

    def proximity_penalty2(self, pos: g.T3value, angle: float) -> float:
        """
        Calculates a 'safe driving penalty' (used as negative rew.)
        as described in Issue #24

        Describes the amount of overlap between the "safety circles" (circles
        that extend further out than BBoxes, giving an earlier collision 'signal'
        The number is max(0, prox.penalty), where a lower (more negative) penalty
        means that more of the circles are overlapping
        """

        pos = _actual_center(pos, angle)
        if len(self.collidable_centers) == 0:
            static_dist = 0

        # Find safety penalty w.r.t static obstacles
        else:
            d = np.linalg.norm(self.collidable_centers - pos, axis=1)

            if not safety_circle_intersection(d, AGENT_SAFETY_RAD, self.collidable_safety_radii):
                static_dist = 0.0
            else:
                static_dist = safety_circle_overlap(d, AGENT_SAFETY_RAD, self.collidable_safety_radii)

        total_safety_pen = static_dist
        for obj in self.objects:
            # Find safety penalty w.r.t dynamic obstacles
            total_safety_pen += obj.proximity(pos, AGENT_SAFETY_RAD)

        return total_safety_pen

    def _inconvenient_spawn(self, pos, agent=None):
        """
        Check that agent spawn is not too close to any object
        """

        results = [
            np.linalg.norm(x.pos - pos) < max(x.max_coords) * 0.5 * x.scale + MIN_SPAWN_OBJ_DIST
            for x in self.objects
            if x.visible 
        ]
        if not agent:
            return np.any(results)
        else:
            too_close = False
            for other_agent in self.agents:
                if other_agent.agent_id != agent.agent_id:
                    distance = np.linalg.norm(np.array(other_agent.cur_pos) - np.array(pos))

                    if distance > 0 and distance < self.robot_length/2:
                        if self.verbose:
                            print(f"Condition: {self.robot_length}")
                            print(f"Distance: {distance}")
                            print(f"Other agent pos: {other_agent.cur_pos}")
                            print(f"Proposed pos: {pos}")
                        too_close = True
            return too_close




    def _collision(self, this_agent_corners, this_agent, learning):
        """
        Tensor-based OBB Collision detection
        """
        # Generate the norms corresponding to each face of BB
        this_agent_norm = generate_norm(this_agent_corners)

        # Check collisions with Static Objects
        if len(self.collidable_corners) > 0:
            collision = intersects(this_agent_corners, self.collidable_corners, this_agent_norm, self.collidable_norms)
            if collision:
                return True

        # Check collisions with Dynamic Objects
        for obj in self.objects:
            if obj.check_collision(this_agent_corners, this_agent_norm):
                return True

        # Check collisions with Agents
        for agent in self.agents:
            if agent != this_agent:
                pos = _actual_center(agent.cur_pos, agent.cur_angle)
                agent_corners = get_agent_corners(pos, agent.cur_angle)
                agent_norm = generate_norm(agent_corners)
                if intersects_single_obj(this_agent_corners, agent_corners.T, this_agent_norm, agent_norm):
                    if learning:
                        return agent
                    else:
                        return True
        # No collision with any object
        return False

    def _valid_pose(self, pos: g.T3value, angle: float, agent: Agent, safety_factor: float = DEFAULT_SAFETY_FACTOR, learning: bool = False) -> bool:
        """
        Check that the agent is in a valid pose

        safety_factor = minimum distance
        """

        # Compute the coordinates of the base of both wheels
        pos = _actual_center(pos, angle)
        f_vec = get_dir_vec(angle)
        r_vec = get_right_vec(angle)

        l_pos = pos - (safety_factor * 0.5 * ROBOT_WIDTH) * r_vec
        r_pos = pos + (safety_factor * 0.5 * ROBOT_WIDTH) * r_vec
        f_pos = pos + (safety_factor * 0.5 * ROBOT_LENGTH) * f_vec

        # Check that the center position and
        # both wheels are on drivable tiles and no collisions

        all_drivable = (
            self._drivable_pos(pos)
        )

        # Recompute the bounding boxes (BB) for the agent
        agent_corners = get_agent_corners(pos, angle)
        if learning:
            collisions = self._collision(agent_corners, agent, learning)
            return all_drivable, collisions
        else:
            no_collision = not self._collision(agent_corners, agent, learning)
            res = no_collision and all_drivable
            if not res and self.verbose:
                logger.info(f"Invalid pose. Collision free: {no_collision} On drivable area: {all_drivable}")
                logger.info(f"safety_factor: {safety_factor}")
                logger.info(f"pos: {pos}")
                logger.info(f"l_pos: {l_pos}")
                logger.info(f"r_pos: {r_pos}")
                logger.info(f"f_pos: {f_pos}")
            return res

        
    def _check_intersection_static_obstacles(self, pos: g.T3value, angle: float) -> bool:
        agent_corners = get_agent_corners(pos, angle)
        agent_norm = generate_norm(agent_corners)
        # Check collisions with Static Objects
        if len(self.collidable_corners) > 0:
            collision = intersects(agent_corners, self.collidable_corners, agent_norm, self.collidable_norms)
            if collision:
                return True
        return False

    def update_physics(self, action, agent, delta_time: float = None):
        action_name = action[1]
        action = action[0]
        if delta_time is None:
            delta_time = self.delta_time

        # Update the robot's position
        agent.prev_pos = agent.cur_pos
        agent.wheelVels = action * self.robot_speed * 1
        agent.cur_pos, agent.cur_angle = self._update_pos(action, agent)
        agent.last_action = action_name

        # Compute the robot's speed
        delta_pos = agent.cur_pos - agent.prev_pos
        agent.speed = np.linalg.norm(delta_pos) / delta_time

        agent.step_count += 1
        agent.timestamp += delta_time

        # Update world objects
        for obj in self.objects:
            if obj.kind == MapFormat1Constants.KIND_DUCKIEBOT:
                if not obj.static:
                    obj_i, obj_j = self.get_grid_coords(obj.pos)
                    same_tile_obj = [
                        o
                        for o in self.objects
                        if tuple(self.get_grid_coords(o.pos)) == (obj_i, obj_j) and o != obj
                    ]

                    if not obj.agent:
                        obj.step_duckiebot(delta_time, self.closest_curve_point, same_tile_obj)
                    elif obj.agent:
                        obj.step_duckiebot_agent(delta_time, same_tile_obj)
            else:
                obj.step(delta_time)

    
    # Get position distance
    def pos_distance(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1)-np.array(pos2)) 

    def cartesian_from_weird(self, pos, angle) -> np.ndarray:
        gx, gy, gz = pos
        grid_height = self.grid_height
        tile_size = self.road_tile_size

        cp = [gx, grid_height * tile_size - gz]

        return geometry.SE2_from_translation_angle(np.array(cp), angle)

    def weird_from_cartesian(self, q: SE2value) -> Tuple[list, float]:
        cp, angle = geometry.translation_angle_from_SE2(q)

        gx = cp[0]
        gy = 0
        GH = self.grid_height
        tile_size = self.road_tile_size
        gz = GH * tile_size - cp[1]
        return [gx, gy, gz], angle

    def compute_reward(self, pos, angle, speed):
        # Compute the collision avoidance penalty
        col_penalty = self.proximity_penalty2(pos, angle)

        # Get the position relative to the right lane tangent
        try:
            lp = self.get_lane_pos2(pos, angle)
        except NotInLane:
            reward = 40 * col_penalty
        else:

            # Compute the reward
            reward = +1.0 * speed * lp.dot_dir + -10 * np.abs(lp.dist) + +40 * col_penalty
        return reward

    def step(self, learning: bool=False):
        for agent in self.agents:
            action = agent.get_next_action()
            if not action:
                continue
            action_name = action[1]
            action = action[0]
            vel, angle = action

            # Distance between the wheels
            baseline = self.unwrapped.wheel_dist

            # assuming same motor constants k for both motors
            k_r = self.k
            k_l = self.k

            # adjusting k by gain and trim
            k_r_inv = (self.gain + self.trim) / k_r
            k_l_inv = (self.gain - self.trim) / k_l

            omega_r = (vel + 0.5 * angle * baseline) / self.radius
            omega_l = (vel - 0.5 * angle * baseline) / self.radius

            # conversion from motor rotation rate to duty cycle
            u_r = omega_r * k_r_inv
            u_l = omega_l * k_l_inv

            # limiting output to limit, which is 1.0 for the duckiebot
            u_r_limited = max(min(u_r, self.limit), -self.limit)
            u_l_limited = max(min(u_l, self.limit), -self.limit)

            vels = np.array([u_l_limited, u_r_limited])

            action = vels
            action = np.clip(action, -1, 1)
            action = np.array(action)
            for _ in range(self.frame_skip):
                self.update_physics([action, action_name], agent)

            misc = agent.get_info(self)

            d = self._compute_done_reward(agent, learning)

            # Put the state into a dictionary
            agent.direction = agent.get_direction(self)
            #agent.get_state(self)
            #agent.get_learning_state(self)

            # Generate the state 
            if learning and agent.in_bounds(self):
                agent.q_state = agent.get_learning_state(self)
            elif learning and d.done:
                agent.q_state = 0
            elif learning and not d.done:
                agent.q_state = 0
            misc["done_code"] = d.done_code

            mine = {}
            mine["k"] = self.k
            mine["gain"] = self.gain
            mine["train"] = self.trim
            mine["radius"] = self.radius
            mine["omega_r"] = omega_r
            mine["omega_l"] = omega_l
            misc["DuckietownEnv"] = mine

            #agent.obs = self.render_obs()
            agent.reward = d.reward
            agent.done = d.done
            agent.misc = misc

        # Initialize the states
        self.get_agents_states()
        
        # Set the new info_struct
        self.c_info_struct = EnvironmentInfo(self)
        
        # Get the relative learning state?
        for agent in self.agents: 
            agent.get_learning_state(self)

        return 

    def _compute_done_reward(self, agent, learning=False) -> DoneRewardInfo:
        reward = 0
        # If the agent is not in a valid pose (on drivable tiles)
        if learning: 
            all_drivable, collision = self._valid_pose(agent.cur_pos, agent.cur_angle, agent, self.safety_factor, learning)
            
            # If not on a tile
            if not all_drivable:
                inbounds = agent.in_bounds(self)
                # If its agent 0 we don't want to reset. It would mark it being done
                if agent.agent_id == "agent0":
                    if not inbounds:
                        done = True
                        done_code = "finished"
                        msg = "%s finished without harm." % agent.agent_id
                        reward = agent.get_reward(self, done_code)
                        #print(msg)
                        return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)
                    if inbounds:
                        done = True
                        done_code = "offroad"
                        msg = "%s drove offroad." % agent.agent_id
                        reward = agent.get_reward(self, done_code)
                        #print(msg)
                        return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)
                else:
                    if not inbounds: # Keep going and reset if our agent drives off
                        done=False
                        done_code = "in-progress"
                        msg = "%s is being reset." % agent.agent_id
                        reward = agent.get_reward(self, done_code)
                        directions = ['N', 'N',  'S', 'S', 'E', 'E', 'W', 'W']
                        colors = ['green', 'red', 'grey', 'cyan', 'yellow', 'orange', 'midnight']
                        if agent.random_spawn:
                            self.spawn_random_agent(agent, directions, colors)
                            # Keep trying to find a valid spawn position on this tile
                        #print(msg)
                        return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)

            # If there was a collision
            if collision:
                if agent.agent_id == "agent0" or collision.agent_id == "agent0":
                    done = True
                    done_code = "collision"
                    msg = "%s collided with %s" % (agent.agent_id, collision.agent_id)
                    reward = agent.get_reward(self, done_code)
                    return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)
                else:
                    done=False
                    done_code = "in-progress"
                    msg = "Resetting agents %s  and %s" % (agent.agent_id, collision.agent_id)
                    reward = agent.get_reward(self, done_code)

                    directions = ['N', 'N',  'S', 'S', 'E', 'E', 'W', 'W']
                    colors = ['green', 'red', 'grey', 'cyan', 'yellow', 'orange', 'midnight']
                    if agent.random_spawn:
                        self.spawn_random_agent(agent, directions, colors)
                    if collision.random_spawn:
                        self.spawn_random_agent(collision, directions, colors)
                    return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)

            if agent.step_count >= self.max_steps:
                done = True
                done_code = "max-steps-reached"
                msg = "Stopping the simulator because we reached max_steps = %s" % self.max_steps
                reward = agent.get_reward(self, done_code)
                return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)

            done = False
            done_code = "in-progress"
            msg = "in progress."
            reward = agent.get_reward(self, done_code)
            return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)
        
        # If not learning
        else:
            if not self._valid_pose(agent.cur_pos, agent.cur_angle, agent, self.safety_factor, learning):
                done = True
                done_code = "invalid-pose"
                msg = "Stopping the simulator because we are at an invalid pose."
                reward = REWARD_INVALID_POSE
                return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)

            # If the maximum time step count is reached
            if agent.step_count >= self.max_steps:
                done = True
                done_code = "max-steps-reached"
                msg = "Stopping the simulator because we reached max_steps = %s" % self.max_steps
                reward = REWARD_INVALID_POSE
                return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)
            
            # If going still
            done = False
            done_code = "in-progress"
            msg = ""
            reward = 0
            return DoneRewardInfo(done=done, done_why=msg, reward=reward, done_code=done_code)
        
    def map_jpg(self, segment: bool = False, background: bool = False):
        img = self._render_img(
            self.camera_width,
            self.camera_height,
            self.multi_fbo,
            self.final_fbo,
            self.img_array,
            top_down=True,
            segment=segment,
            only_map=True,
        )

        if not background:
            img = Image.fromarray(img, 'RGB')
            nonwhite_positions = [(x,y) for x in range(img.size[0]) for y in range(img.size[1]) if img.getdata()[x+y*img.size[0]] != (255,0,255)]
            rect = (min([x for x,y in nonwhite_positions]), min([y for x,y in nonwhite_positions]), max([x for x,y in nonwhite_positions]), max([y for x,y in nonwhite_positions]))
            image_path = "src/webserver/images"
            image = img.crop(rect).save(f"{image_path}/empty_map.jpg")
        else:
            img = Image.fromarray(img, 'RGB')
            width, height = img.size
            for x in range(0, width):
                for y in range(0, height):
                    current_color = img.getpixel((x,y))
                    if current_color == (255,  0 , 255):
                        img.putpixel((x,y), (38, 38, 38))
                    
            image_path = "src/webserver/images"
            image = img.save(f"{image_path}/empty_map_background.jpg")

        return image


    
    def _render_img(
        self,
        width: int,
        height: int,
        multi_fbo,
        final_fbo,
        img_array,
        top_down: bool = True,
        segment: bool = False,
        only_map: bool = False,
    ) -> np.ndarray:
        """
        Render an image of the environment into a frame buffer
        Produce a numpy RGB array image as output
        """

        if not self.graphics:
            return np.zeros((height, width, 3), np.uint8)

        # Switch to the default context
        # This is necessary on Linux nvidia drivers
        # pyglet.gl._shadow_window.switch_to()
        self.shadow_window.switch_to()

        if segment:
            gl.glDisable(gl.GL_LIGHT0)
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_COLOR_MATERIAL)
        else:
            gl.glEnable(gl.GL_LIGHT0)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_COLOR_MATERIAL)

        # note by default the ambient light is 0.2,0.2,0.2
        ambient = [0.3, 0.3, 0.3, 1.0]

        gl.glEnable(gl.GL_POLYGON_SMOOTH)

        gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, (gl.GLfloat * 4)(*ambient))
        # Bind the multisampled frame buffer
        gl.glEnable(gl.GL_MULTISAMPLE)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, multi_fbo)
        gl.glViewport(0, 0, width, height)

        # Clear the color and depth buffers
        c0, c1, c2 = self.horizon_color if not segment else [255, 0, 255]
        gl.glClearColor(c0, c1, c2, 1.0)
        gl.glClearDepth(1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Set the projection matrix
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(self.cam_fov_y, width / float(height), 0.04, 100.0)

        # Set modelview matrix
        # Note: we add a bit of noise to the camera position for data augmentation
        pos = self.agents[0].cur_pos
        angle = self.agents[0].cur_angle

        if self.domain_rand:
            pos = pos + self.randomization_settings["camera_noise"]

        x, y, z = pos + self.cam_offset
        dx, dy, dz = get_dir_vec(angle)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        if not top_down:
            y += self.cam_height
            gl.glRotatef(self.cam_angle[0], 1, 0, 0)
            gl.glRotatef(self.cam_angle[1], 0, 1, 0)
            gl.glRotatef(self.cam_angle[2], 0, 0, 1)
            gl.glTranslatef(0, 0, CAMERA_FORWARD_DIST)
        elif top_down:
            a = (self.grid_width * self.road_tile_size) / 2
            b = (self.grid_height * self.road_tile_size) / 2
            
            fov_y_deg = self.cam_fov_y
            fov_y_rad = np.deg2rad(fov_y_deg)
            H_to_fit = max(a, b) + 0.3  # borders

            H_FROM_FLOOR = H_to_fit / (np.tan(fov_y_rad / 2)) 

            look_from = a, H_FROM_FLOOR, b
            look_at = a, 0.0, b - 0.0000001
            up_vector = 0.0, 1.0, 0
            gl.gluLookAt(*look_from, *look_at, *up_vector)
            
        else:
            look_from = x, y, z
            look_at = x + dx, y + dy, z + dz
            up_vector = 0.0, 1.0, 0.0
            gl.gluLookAt(*look_from, *look_at, *up_vector)

        # Draw the ground quad
        gl.glDisable(gl.GL_TEXTURE_2D)

        # background is magenta when segmenting for easy isolation of main map image
        if not only_map:
            gl.glColor3f(*self.ground_color if not segment else [255, 0, 255])  # XXX
        else:
            gl.glColor3f(255, 0, 255)  # XXX
        gl.glPushMatrix()
        gl.glScalef(50, 0.01, 50)
        self.ground_vlist.draw(gl.GL_QUADS)

        gl.glPopMatrix()

        # Draw the ground/noise triangles
        if not segment:
            gl.glPushMatrix()
            gl.glTranslatef(0.0, 0.1, 0.0)
            self.tri_vlist.draw(gl.GL_TRIANGLES)
            gl.glPopMatrix()

        # Draw the road quads
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        add_lights = False

        if add_lights:
            for i in range(1):
                li = gl.GL_LIGHT0 + 1 + i
                # li_pos = [i + 1, 1, i + 1, 1]

                li_pos = [0.0, 0.2, 3.0, 1.0]
                diffuse = [0.0, 0.0, 1.0, 1.0] if i % 2 == 0 else [1.0, 0.0, 0.0, 1.0]
                ambient = [0.0, 0.0, 0.0, 1.0]
                specular = [0.0, 0.0, 0.0, 1.0]
                spot_direction = [0.0, -1.0, 0.0]
                
                if self.verbose:
                    logger.debug(
                        li=li, li_pos=li_pos, ambient=ambient, diffuse=diffuse, spot_direction=spot_direction
                    )
                gl.glLightfv(li, gl.GL_POSITION, (gl.GLfloat * 4)(*li_pos))
                gl.glLightfv(li, gl.GL_AMBIENT, (gl.GLfloat * 4)(*ambient))
                gl.glLightfv(li, gl.GL_DIFFUSE, (gl.GLfloat * 4)(*diffuse))
                gl.glLightfv(li, gl.GL_SPECULAR, (gl.GLfloat * 4)(*specular))
                gl.glLightfv(li, gl.GL_SPOT_DIRECTION, (gl.GLfloat * 3)(*spot_direction))
                gl.glLightf(li, gl.GL_SPOT_CUTOFF, 60)

                gl.glLightfv(li, gl.GL_CONSTANT_ATTENUATION, (gl.GLfloat * 1)(1.0))
                gl.glLightfv(li, gl.GL_QUADRATIC_ATTENUATION, (gl.GLfloat * 1)(0.2))
                gl.glEnable(li)


        # For each grid tile
        for i, j in itertools.product(range(self.grid_width), range(self.grid_height)):

            # Get the tile type and angle
            tile = self._get_tile(i, j)

            if tile is None:
                continue

            # kind = tile['kind']
            angle = tile["angle"]
            color = tile["color"]
            texture = tile["texture"]

            gl.glColor4f(*color)
            gl.glPushMatrix()

            TS = self.road_tile_size
            gl.glTranslatef((i + 0.5) * TS, 0, (j + 0.5) * TS)
            gl.glRotatef(angle * 90 + 180, 0, 1, 0)

            # Bind the appropriate texture
            texture.bind(segment)

            self.road_vlist.draw(gl.GL_QUADS)

            gl.glPopMatrix()

            if self.draw_curve and tile["drivable"]:

                # Find curve with largest dotproduct with heading
                gl.glPushMatrix()

                TS = self.road_tile_size
                gl.glTranslatef(0, 0.1, 0)
                curves = tile["curves"]
                curve_headings = curves[:, -1, :] - curves[:, 0, :]
                curve_headings = curve_headings / np.linalg.norm(curve_headings).reshape(1, -1)
                dirVec = get_dir_vec(self.agents[0].cur_angle)
                dot_prods = np.dot(curve_headings, dirVec)

                # Current ("closest") curve drawn in Red
                if tile['kind'] == '4way':
                    pts = curves[1]
                else:
                    pts = curves[np.argmax(dot_prods)]
                bezier_draw(pts, n=20)

                pts = self._get_curve(i, j)
                for idx, pt in enumerate(pts):
                    bezier_draw(pt, n=20)

                gl.glPopMatrix()

        if not only_map:
            # For each object
            for obj in self.objects:
                obj.render(draw_bbox=self.draw_bbox, segment=segment, enable_leds=self.enable_leds)

            # Draw the agent's own bounding box
            for agent in self.agents:
                pos = agent.cur_pos
                angle = agent.cur_angle
         
                if self.draw_bbox:
                    corners = get_agent_corners(pos, angle, bbox_offset_w=agent.bbox_offset_w, bbox_offset_l=agent.bbox_offset_l)
                    gl.glColor3f(0, .9, .9)
                    gl.glBegin(gl.GL_LINE_LOOP)
                    gl.glVertex3f(corners[0, 0], .01, corners[0, 1])
                    gl.glVertex3f(corners[1, 0], .01, corners[1, 1])
                    gl.glVertex3f(corners[2, 0], .01, corners[2, 1])
                    gl.glVertex3f(corners[3, 0], .01, corners[3, 1])
                    gl.glEnd()
                
                gl.glPushMatrix()
                gl.glTranslatef(*agent.cur_pos)
                gl.glScalef(1, 1, 1)
                gl.glRotatef(agent.cur_angle * 180 / np.pi, 0, 1, 0)
                agent.mesh.render()


                # Handle lights
                if self.enable_leds:
                    s_main = 0.01  # 1 cm sphere
                    s_halo = 0.04
                    
                    colors = {
                        "center": (1, 1, 0),
                        "front_left": (1, 1, 0),
                        "front_right": (1, 1, 0),
                        "back_left": (1, 1, 0),
                        "back_right": (1, 1, 0),
                    }

                    for light_name, (px, py, pz, led_on) in agent.lights.items():
                        if led_on:
                            color = np.clip(colors[light_name], 0, +1)
                            color_intensity = float(np.mean(color))
                            gl.glPushMatrix()

                            gl.glTranslatef(px, pz, py)

                            gl.glEnable(gl.GL_BLEND)
                            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)

                            sphere = gluNewQuadric()

                            gl.glColor4f(color[0], color[1], color[2], 1.0)
                            gluSphere(sphere, s_main, 10, 10)

                            gl.glColor4f(color[0], color[1], color[2], 0.2)

                            s_halo_effective = color_intensity * s_halo

                            gluSphere(sphere, s_halo_effective, 10, 10)

                            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
                            gl.glBlendFunc(gl.GL_ONE, gl.GL_ZERO)
                            gl.glDisable(gl.GL_BLEND)

                            gl.glPopMatrix()      
                
                    gl.glPopMatrix()

                draw_xyz_axes = False

                if draw_xyz_axes:
                    draw_axes()

        
        # Resolve the multisampled frame buffer into the final frame buffer
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, multi_fbo)
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, final_fbo)
        gl.glBlitFramebuffer(0, 0, width, height, 0, 0, width, height, gl.GL_COLOR_BUFFER_BIT, gl.GL_LINEAR)

        # Copy the frame buffer contents into a numpy array
        # Note: glReadPixels reads starting from the lower left corner
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, final_fbo)
        gl.glReadPixels(
            0, 0, width, height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_array.ctypes.data_as(POINTER(gl.GLubyte))
        )

        # Unbind the frame buffer
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

        # Flip the image because OpenGL maps (0,0) to the lower-left corner
        # Note: this is necessary for gym.wrappers.Monitor to record videos
        # properly, otherwise they are vertically inverted.
        img_array = np.ascontiguousarray(np.flip(img_array, axis=0))

        return img_array

    def render_obs(self, segment: bool = False) -> np.ndarray:
        """
        Render an observation from the point of view of the agent
        """

        observation = self._render_img(
            self.camera_width,
            self.camera_height,
            self.multi_fbo,
            self.final_fbo,
            self.img_array,
            top_down=False,
            segment=segment,
        )

        if self.distortion and not self.undistort:
            observation = self.camera_model.distort(observation)

        return observation

    def render(self, mode: str = "human", close: bool = False, segment: bool = False):
        """
        Render the environment for human viewing

        mode: "human", "top_down", "free_cam", "rgb_array"

        """
        assert mode in ["human", "top_down", "free_cam", "rgb_array"]

        if close:
            if self.window:
                self.window.close()
                self.text_window.close()
            return

        top_down = mode == "top_down"

        # Render the image
        img = self._render_img(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            self.multi_fbo_human,
            self.final_fbo_human,
            self.img_array_human,
            top_down=top_down,
            segment=segment,
        )

        # Save the image to the directory
        web_img = Image.fromarray(img, 'RGB')
        image_path = "src/webserver/images"
        web_img.save(f"{image_path}/rendered_scene.jpg")

        if self.distortion and not self.undistort and mode != "free_cam":
            img = self.camera_model.distort(img)

        if mode == "rgb_array":
            return img

        if self.window is None:
            config = gl.Config(double_buffer=False)
            self.window = window.Window(
                width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=True, config=config
            )
            self.text_window = window.Window(
                width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=True, config=config
            )
        self.text_window.clear()
        self.text_window.switch_to()
        self.text_window.dispatch_events()
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()

        # Bind the default frame buffer
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

        # Setup orghogonal projection
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
        

        # Draw the image to the rendering window
        width = img.shape[1]
        height = img.shape[0]
        img = np.ascontiguousarray(np.flip(img, axis=0))
        img_data = image.ImageData(
            width,
            height,
            "RGB",
            img.ctypes.data_as(POINTER(gl.GLubyte)),
            pitch=width * 3,
        )
        img_data.blit(0, 0, 0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

       
        # Display position/state information
        if mode != "free_cam":
            starting_x = 0
            self.text_window.switch_to()
            for agent in self.agents:
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y= 20 * 20)
                stat.text = (f"Agent {agent.index}, {agent.color}, Step: {agent.step_count}")
                stat.draw()  
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 19)
                x, y, z = agent.cur_pos
                stat.text = (f"pos: ({x:.2f}, {y:.2f}, {z:.2f})")
                stat.draw()  
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 18)
                stat.text = (f"angle: {np.rad2deg(self.agents[0].cur_angle):.1f} direction: {agent.direction} ")
                stat.draw()  
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 17)
                stat.text = (f"speed: {agent.speed:.2f}")
                stat.draw()  
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 16)
                stat.text = (f"forward_step: {agent.forward_step:.2f}")
                stat.draw()  
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 15)
                stat.text = (f"turn: {agent.turn_choice} signal: {agent.signal_choice}")
                stat.draw()  
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 14)
                stat.text = (f"patience: {agent.patience} int_arrival: {agent.intersection_arrival}")
                stat.draw()  
                #0 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 13)
                stat.text = (f"in_int: {agent.states['in_intersection']}")
                stat.draw()  
                #1 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 12)
                stat.text = (f"at_int: {agent.states['at_intersection_entry']}")
                stat.draw()  
                #2 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 11)
                stat.text = (f"empty_int: {agent.states['intersection_empty']}")
                stat.draw()  
                #3 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 10)
                stat.text = (f"appr_int: {agent.states['approaching_intersection']}")
                stat.draw()  
                #4 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 9)
                stat.text = (f"obj_in_range: {agent.states['obj_in_range']}")
                stat.draw()  
                #5 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 8)
                stat.text = (f"has_right_of_way: {agent.states['has_right_of_way']}")
                stat.draw()  
                #6 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 7)
                stat.text = (f"cars_waiting_to_enter: {agent.states['cars_waiting_to_enter']}")
                stat.draw()  
                #7 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 6)
                stat.text = (f"car_entering_range: {agent.states['car_entering_range']}")
                stat.draw()  
                #8 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 5)
                stat.text = (f"safe_to_enter: {agent.states['safe_to_enter']}")
                stat.draw()  
                #9 
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 4)
                stat.text = (f"is_tailgating: {agent.states['is_tailgating']}")
                stat.draw()  
                #10
                stat = pyglet.text.Label(font_name="Arial", font_size=9, x=200*starting_x, y=20 * 3)
                next_to_go = agent.states["next_to_go"]
                stat.text = (f"next_to_go: {next_to_go}")
                stat.draw()  
                starting_x += 1
            self.text_window.dispatch_events()

        

        # Force execution of queued commands
        gl.glFlush()

        return img

    def _update_pos(self, action, agent):
        """
        Update the position of the robot, simulating differential drive

        returns pos, angle
        """

        action = DynamicsInfo(motor_left=action[0], motor_right=action[1])
        agent.state = agent.state.integrate(self.delta_time, action)
        q = agent.state.TSE2_from_state()[0]
        pos, angle = self.weird_from_cartesian(q)
        pos = np.asarray(pos)
        return pos, angle

    # Spawn a random agent
    def spawn_random_agent(self, agent, directions, colors):
        for _ in range(MAX_SPAWN_ATTEMPTS):
            direction = random.choice(directions)
            if agent.agent_id == "agent0":
                color = "blue"
            else:
                color = random.choice(colors)
            if direction == 'N':
                i, j = 2, 4
            elif direction == 'S':
                i, j = 2, 0
            elif direction == 'E':
                i, j = 0, 2
            elif direction == 'W':
                i, j = 4, 2
            turn_choices = ['Right', 'Left', 'Straight']
            turn_choice = random.choice(turn_choices)
            agent.turn_choice = turn_choice
            agent.signal_choice = turn_choice

            agent.color = color
            agent.mesh = get_duckiebot_mesh(agent.color)
            agent.forward_step = round(self.np_random.uniform(0.35, 0.6), 2)
            agent.patience = 0

            # Choose a random position on this tile
            if direction == 'N':
                perturb_x = 3/4 * self.road_tile_size   # Right side of the road
                perturb_z = self.np_random.uniform(0.01, .9) * self.road_tile_size
                x = perturb_x + i * self.road_tile_size
                z = perturb_z + j * self.road_tile_size
                base_angle = 90
            elif direction == 'S':
                perturb_x = 1/4 * self.road_tile_size   # Right side of the road
                perturb_z = self.np_random.uniform(0.01, .9) * self.road_tile_size
                x = perturb_x + i * self.road_tile_size
                z = perturb_z + j * self.road_tile_size
                base_angle = 270
            elif direction == 'E':
                perturb_x = self.np_random.uniform(0.01, .9) * self.road_tile_size 
                perturb_z = 3/4 * self.road_tile_size   # Right side of the road
                x = perturb_x + i * self.road_tile_size
                z = perturb_z + j * self.road_tile_size
                base_angle = 360
            elif direction == 'W':
                perturb_x = self.np_random.uniform(0.01, 0.9) * self.road_tile_size 
                perturb_z = 1/4 * self.road_tile_size   # Right side of the road
                x = perturb_x + i * self.road_tile_size
                z = perturb_z + j * self.road_tile_size
                base_angle = 180

            # Choose a random position and direction to face
            propose_pos = np.array([x, 0, z])
            propose_angle = math.radians(base_angle) 

            # If this is too close to an object or not a valid pose, retry
            inconvenient = self._inconvenient_spawn(propose_pos, agent)

            if inconvenient:
                # msg = 'The spawn was inconvenient.'
                # logger.warning(msg)
                continue

            invalid = not self._valid_pose(propose_pos, propose_angle, agent, safety_factor=1.3)
            if invalid:
                # msg = 'The spawn was invalid.'
                # logger.warning(msg)
                continue

            # Found a valid initial pose
            break
        else:
            msg = f"Could not find a valid starting pose for {agent.agent_id} after {MAX_SPAWN_ATTEMPTS} attempts"
            logger.warn(msg)
            raise Exception(msg)

        # Initialize agent
        agent.cur_pos = propose_pos
        agent.prev_pos = propose_pos
        agent.cur_angle = propose_angle
        agent.curve = agent.get_curve(self)
        agent.start_direction = agent.get_direction(self)
        agent.actions = []
        agent.intersection_arrival = -1
        agent.nearby_objects = []
        agent.nearby_agents = []
        agent.last_action = None
        agent.tiles_visited = set()
        agent.wheelVels = np.array([0.0, 0.0]) 

        # Initialize Dynamics model
        init_vel = np.array([0, 0])
        if self.dynamics_rand:
            trim = 0 + self.randomization_settings["trim"][0]
            p = get_DB18_uncalibrated(delay=0.15, trim=trim)
        else:
            p = get_DB18_nominal(delay=0.15)

        q = self.cartesian_from_weird(agent.cur_pos, agent.cur_angle)
        v0 = geometry.se2_from_linear_angular(init_vel, 0)
        c0 = q, v0
        agent.state = p.initialize(c0=c0, t0=0)

        # SEt the lights 
        agent.intersection_arrival = -1
        agent.lights["front_left"][3] = False
        agent.lights["front_right"][3] = False
        agent.lights["back_left"][3] = False
        agent.lights["back_right"][3] = False
        agent.lights["center"][3] = False
        
        # Set the states
        agent.states['in_intersection'] = False
        agent.states['at_intersection_entry'] = False
        agent.states['intersection_empty'] = False
        agent.states['approaching_intersection'] = False
        agent.states['obj_in_range'] = False
        agent.states['has_right_of_way'] = False
        agent.states['cars_waiting_to_enter'] = False
        agent.states['car_entering_range'] = False
        agent.states['obj_behind_intersection'] = False
        agent.states['obj_behind_no_intersection'] = False
        agent.states['is_tailgating'] = False
        agent.states['next_to_go'] = False
        agent.states['safe_to_enter'] = False
        


    def get_agent_corners(self, pos, angle, bbox_offset_w = 0, bbox_offset_l = 0):
        agent_corners = agent_boundbox(
            _actual_center(pos, angle), ROBOT_WIDTH + bbox_offset_w, ROBOT_LENGTH + bbox_offset_l, get_dir_vec(angle), get_right_vec(angle)
        )
        return agent_corners

def get_dir_vec(cur_angle: float) -> np.ndarray:
    """
    Vector pointing in the direction the agent is looking
    """

    x = math.cos(cur_angle)
    z = -math.sin(cur_angle)
    return np.array([x, 0, z])


def get_right_vec(cur_angle: float) -> np.ndarray:
    """
    Vector pointing to the right of the agent
    """

    x = math.sin(cur_angle)
    z = math.cos(cur_angle)
    return np.array([x, 0, z])



def _actual_center(pos, angle):
    """
    Calculate the position of the geometric center of the agent
    The value of self.cur_pos is the center of rotation.
    """

    dir_vec = get_dir_vec(angle)
    return pos + (CAMERA_FORWARD_DIST - (ROBOT_LENGTH / 2)) * dir_vec


def get_agent_corners(pos, angle, bbox_offset_w = 0, bbox_offset_l = 0):
    agent_corners = agent_boundbox(
        _actual_center(pos, angle), ROBOT_WIDTH + bbox_offset_w, ROBOT_LENGTH + bbox_offset_l, get_dir_vec(angle), get_right_vec(angle)
    )
    return agent_corners

       
class FrameBufferMemory:
    multi_fbo: int
    final_fbo: int
    img_array: np.ndarray
    width: int

    height: int

    def __init__(self, *, width: int, height: int):
        """H, W"""
        self.width = width
        self.height = height

        # that's right, it's inverted
        self.multi_fbo, self.final_fbo = create_frame_buffers(width, height, 4)
        self.img_array = np.zeros(shape=(height, width, 3), dtype=np.uint8)


def draw_axes():
    gl.glPushMatrix()
    gl.glLineWidth(4.0)
    gl.glTranslatef(0.0, 0.0, 0.0)
    gl.glBegin(gl.GL_LINES)
    L = 1.0

    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glVertex3f(0.0, 0.0, 0.0)
    gl.glVertex3f(L, 0.0, 0.0)

    gl.glColor3f(0.0, 1.0, 0.0)
    gl.glVertex3f(0.0, 0.0, 0.0)
    gl.glVertex3f(0.0, L, 0.0)

    gl.glColor3f(0.0, 0.0, 1.0)
    gl.glVertex3f(0.0, 0.0, 0.0)
    gl.glVertex3f(0.0, 0.0, L)

    gl.glEnd()

    gl.glPopMatrix()

