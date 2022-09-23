from ctypes import *
from enum import IntEnum

class Action(IntEnum):
    NO_ACTION = 0
    STOP = 1
    SLOW_DOWN = 2
    FORWARD_STEP = 3
    INTERSECTION_STOP = 4
    INTERSECTION_FORWARD = 5
    INTERSECTION_LEFT = 6
    INTERSECTION_RIGHT = 7


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

class AgentState(Structure):
    _fields_ = [('in_intersection', c_bool),
                ('at_entry', c_bool),
                ('intersection_empty', c_bool),
                ('intersection_in_range', c_bool),
                ('object_in_range', c_bool),
                ('ahead_car_intersection_in_range', c_bool),
                ('ahead_car_object_in_range', c_bool),
                ('car_entering_our_range', c_bool),
                ('car_behind_us_in_intersection', c_bool),
                ('car_behind_us_out_intersection', c_bool)]


class IntersectionAction(Structure):
    _fields_ = [('turn_choice', c_int),
                ('signal_choice', c_int),
                ('action', c_int),
                ('wait_step', c_int)]

class EnvironmentAgent(Structure):
    _fields_ = [('pos_x', c_float),
                ('pos_z', c_float),
                ('angle', c_float),
                ('distance_away', c_float),
                ('direction', c_int),
                ('intersection_arrival', c_int)]

class EnvironmentAgentArray(Structure):
    _fields_ = [('elements', c_int),
                ('ENV_AGENT_ARRAY', POINTER(EnvironmentAgent))]


    def __init__(self, env, intersection_agents, our_agent):
        num_intersection_agents = int(len(intersection_agents))
        elems = (EnvironmentAgent * num_intersection_agents)() # Size
        self.ENV_AGENT_ARRAY = cast(elems, POINTER(EnvironmentAgent))
        self.elements = num_intersection_agents

        for i, agent in enumerate(intersection_agents):
            self.ENV_AGENT_ARRAY[i].pos_x = float(agent.cur_pos[0])
            self.ENV_AGENT_ARRAY[i].pos_z = float(agent.cur_pos[2])
            self.ENV_AGENT_ARRAY[i].angle = float(agent.cur_angle)
            self.ENV_AGENT_ARRAY[i].distance_away = float(env.pos_distance(our_agent.get_curr_pos(env, matrix=True), \
                                             agent.get_curr_pos(env, matrix=True)))
            self.ENV_AGENT_ARRAY[i].direction = get_dl_direction(agent.get_direction(env))
            self.ENV_AGENT_ARRAY[i].intersection_arrival = agent.intersection_arrival


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
