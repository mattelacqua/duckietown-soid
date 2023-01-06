from ctypes import *
from enum import IntEnum

class Action(IntEnum):
    NO_ACTION = 0
    STOP = 1
    FORWARD_STEP = 2
    INTERSECTION_STOP = 3
    INTERSECTION_FORWARD = 4

class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
 
class TurnChoice(IntEnum):
    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2
    RANDOM = 3   

class IntersectionAction(Structure):
    _fields_ = [('turn_choice', c_int),
                ('signal_choice', c_int),
                ('action', c_int)]

class AgentState(Structure):
    _fields_ = [('in_intersection', c_bool),
                ('at_intersection_entry', c_bool),
                ('intersection_empty', c_bool),
                ('approaching_intersection', c_bool),
                ('obj_in_range', c_bool),
                ('has_right_of_way', c_bool),
                ('cars_waiting_to_enter', c_bool),
                ('car_entering_range', c_bool),
                ('obj_behind_intersection', c_bool),
                ('is_tailgating', c_bool),
                ('next_to_go', c_bool)]


class EnvironmentAgent(Structure):
    _fields_ = [('id', c_int),
                ('pos_x', c_float),
                ('pos_z', c_float),
                ('prev_pos_x', c_float),
                ('prev_pos_z', c_float),
                ('stop_x', c_float),
                ('stop_z', c_float),
                ('tile_x', c_int),
                ('tile_z', c_int),
                ('angle', c_float),
                ('speed', c_float),
                ('forward_step', c_float),
                ('direction', c_int),
                ('intersection_arrival', c_int),
                ('patience', c_int),
                ('step_count', c_int),
                ('state', AgentState)]


class EnvironmentAgentArray(Structure):
    _fields_ = [('elements', c_int),
                ('ENV_AGENT_ARRAY', POINTER(EnvironmentAgent))]


    def __init__(self, env, agents):
        num_intersection_agents = int(len(agents))
        elems = (EnvironmentAgent * num_intersection_agents)() # Size
        self.ENV_AGENT_ARRAY = cast(elems, POINTER(EnvironmentAgent))
        self.elements = c_int(num_intersection_agents)

        for i, agent in enumerate(agents):
            self.ENV_AGENT_ARRAY[i].id = c_int(agent.index)
            self.ENV_AGENT_ARRAY[i].pos_x = c_float(agent.cur_pos[0])
            self.ENV_AGENT_ARRAY[i].pos_z = c_float(agent.cur_pos[2])

            self.ENV_AGENT_ARRAY[i].prev_pos_x = c_float(agent.prev_pos[0])
            self.ENV_AGENT_ARRAY[i].prev_pos_z = c_float(agent.prev_pos[2])

            stop_x, stop_z = agent.get_stop_pos(env)
            self.ENV_AGENT_ARRAY[i].stop_x = c_float(stop_x)
            self.ENV_AGENT_ARRAY[i].stop_z = c_float(stop_z)

            tile_x, tile_z = list(env.get_grid_coords(agent.cur_pos))
            self.ENV_AGENT_ARRAY[i].tile_x = c_int(tile_x)
            self.ENV_AGENT_ARRAY[i].tile_z = c_int(tile_z)

            self.ENV_AGENT_ARRAY[i].angle = c_float(agent.cur_angle)
            self.ENV_AGENT_ARRAY[i].speed = c_float(agent.speed)
            self.ENV_AGENT_ARRAY[i].forward_step = c_float(agent.forward_step)
            self.ENV_AGENT_ARRAY[i].direction = get_dl_direction(agent.direction)
            self.ENV_AGENT_ARRAY[i].intersection_arrival = c_int(agent.intersection_arrival) if agent.intersection_arrival else c_int(env.max_steps)
            self.ENV_AGENT_ARRAY[i].patience = c_int(agent.patience)
            self.ENV_AGENT_ARRAY[i].step_count = c_int(agent.step_count)

            self.ENV_AGENT_ARRAY[i].state = AgentState(agent.states['in_intersection'],
                                                    agent.states['at_intersection_entry'],
                                                    agent.states['intersection_empty'],
                                                    agent.states['approaching_intersection'],
                                                    agent.states['obj_in_range'],
                                                    agent.states['has_right_of_way'],
                                                    agent.states['cars_waiting_to_enter'],
                                                    agent.states['car_entering_range'],
                                                    agent.states['obj_behind_intersection'],
                                                    agent.states['is_tailgating'],
                                                    agent.next_to_go(env))


class EnvironmentInfo(Structure):
    _fields_ = [('intersection_x', c_int),
                ('intersection_z', c_int),
                ('robot_length', c_float),
                ('grid_w', c_int),
                ('grid_h', c_int),
                ('road_tile_size', c_float),
                ('max_steps', c_int),
                ('agents', EnvironmentAgentArray)]

    def __init__(self, env):
        self.intersection_x = -1
        self.intersection_z = -1
        for tile in env.grid:
            if tile['kind'] == '4way':
                self.intersection_x = tile['coords'][0]
                self.intersection_z = tile['coords'][1]
        self.robot_length = env.robot_length
        self.grid_w = env.grid_width
        self.grid_h = env.grid_height
        self.road_tile_size = env.road_tile_size
        self.max_steps = env.max_steps

        self.agents = EnvironmentAgentArray(env, env.agents)

def get_turn_choice(turn):
    if turn == "Straight":
        return TurnChoice.STRAIGHT
    elif turn == "Left":
        return TurnChoice.LEFT
    elif turn == "Right":
        return TurnChoice.RIGHT
    elif turn == None:
        return TurnChoice.RANDOM

def get_dl_direction(direction):
    if direction == 'N':
        direction = Direction.NORTH
    elif direction == 'S':
        direction = Direction.SOUTH
    elif direction == 'E':
        direction = Direction.EAST
    elif direction == 'W':
        direction = Direction.WEST
    return direction
