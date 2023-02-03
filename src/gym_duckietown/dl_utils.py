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

class TilePos(Structure):
    _fields_ = [('x', c_int),
                ('z', c_int)]

class StopPos(Structure):
    _fields_ = [('x', c_float),
                ('z', c_float)]

class AgentState(Structure):
    _fields_ = [('in_intersection', c_bool),
                ('at_intersection_entry', c_bool),
                ('intersection_empty', c_bool),
                ('approaching_intersection', c_bool),
                ('obj_in_range', c_bool),
                ('has_right_of_way', c_bool),
                ('safe_to_enter', c_bool),
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
                ('initial_direction', c_int),
                ('signal_choice', c_int),
                ('turn_choice', c_int),
                ('intersection_arrival', c_int),
                ('patience', c_int),
                ('step_count', c_int),
                ('lookahead', c_float),
                ('state', AgentState),
                ('q_table', ((c_float * 2) * 1024)),
                ('exists', c_bool)]


class EnvironmentInfo(Structure):
    _fields_ = [('intersection_x', c_int),
                ('intersection_z', c_int),
                ('robot_length', c_float),
                ('grid_w', c_int),
                ('grid_h', c_int),
                ('road_tile_size', c_float),
                ('max_steps', c_int),
                ('num_agents', c_int),
                ('agents', EnvironmentAgent * 8)]

    def __init__(self, env):
        self.intersection_x = -1
        self.intersection_z = -1
        for tile in env.grid:
            if tile['kind'] == '4way':
                self.intersection_x = tile['coords'][0]
                self.intersection_z = tile['coords'][1]
        self.robot_length = round(env.robot_length, 3)
        self.grid_w = env.grid_width
        self.grid_h = env.grid_height
        self.road_tile_size = round(env.road_tile_size, 3)
        self.max_steps = env.max_steps
        self.num_agents = int(len(env.agents))

        for i in range(env.max_agents):
            if i < len(env.agents):
                agent = env.agents[i]
                self.agents[i].id = c_int(agent.index)
                self.agents[i].pos_x = c_float(round(agent.cur_pos[0], 3))
                self.agents[i].pos_z = c_float(round(agent.cur_pos[2], 3))

                self.agents[i].prev_pos_x = c_float(round(agent.prev_pos[0], 3))
                self.agents[i].prev_pos_z = c_float(round(agent.prev_pos[2], 3))

                stop_x, stop_z = agent.get_stop_pos(env)
                self.agents[i].stop_x = c_float(round(stop_x, 3))
                self.agents[i].stop_z = c_float(round(stop_z, 3))

                tile_x, tile_z = list(env.get_grid_coords(agent.cur_pos))
                self.agents[i].tile_x = c_int(tile_x)
                self.agents[i].tile_z = c_int(tile_z)

                self.agents[i].angle = c_float(round(agent.cur_angle, 3))
                self.agents[i].speed = c_float(round(agent.speed, 3))
                self.agents[i].forward_step = c_float(round(agent.forward_step, 3))
                self.agents[i].direction = get_dl_direction(agent.direction)
                self.agents[i].initial_direction = get_dl_direction(agent.initial_direction)
                self.agents[i].signal_choice = get_turn_choice(agent.signal_choice)
                self.agents[i].turn_choice = get_turn_choice(agent.turn_choice)
                self.agents[i].intersection_arrival = c_int(agent.intersection_arrival) 
                self.agents[i].patience = c_int(agent.patience)
                self.agents[i].step_count = c_int(round(agent.step_count, 3))
                self.agents[i].lookahead = c_float(round(agent.lookahead, 3))

                self.agents[i].state = AgentState(agent.states['in_intersection'],
                                                        agent.states['at_intersection_entry'],
                                                        agent.states['intersection_empty'],
                                                        agent.states['approaching_intersection'],
                                                        agent.states['obj_in_range'],
                                                        agent.states['has_right_of_way'],
                                                        agent.states['safe_to_enter'],
                                                        agent.states['cars_waiting_to_enter'],
                                                        agent.states['car_entering_range'],
                                                        agent.states['obj_behind_intersection'],
                                                        agent.states['is_tailgating'],
                                                        agent.states['next_to_go'])
                
                # handle q table
                table_spaces = ((c_float * 2) * 1024)() # Size
                self.agents[i].q_table = table_spaces
                for m in range(1024):
                    for n in range(2):
                        self.agents[i].q_table[m][n] = c_float(agent.q_table.qt[m][n])

                self.agents[i].exists = c_bool(True)
            else:
                self.agents[i].id = c_int(-1)
                self.agents[i].pos_x = c_float(-1.0)
                self.agents[i].pos_z = c_float(-1.0)

                self.agents[i].prev_pos_x = c_float(-1.0)
                self.agents[i].prev_pos_z = c_float(-1.0)

                self.agents[i].stop_x = c_float(-1.0)
                self.agents[i].stop_z = c_float(-1.0)

                self.agents[i].tile_x = c_int(-1)
                self.agents[i].tile_z = c_int(-1)

                self.agents[i].angle = c_float(0.0)
                self.agents[i].speed = c_float(0.0)
                self.agents[i].forward_step = c_float(0.0)
                self.agents[i].direction = Direction.NORTH
                self.agents[i].initial_direction = Direction.NORTH
                self.agents[i].signal_choice = TurnChoice.STRAIGHT
                self.agents[i].turn_choice = TurnChoice.STRAIGHT
                self.agents[i].intersection_arrival = c_int(-1)
                self.agents[i].patience = c_int(-1)
                self.agents[i].step_count = c_int(-1)
                self.agents[i].lookahead = c_float(-1.0)

                self.agents[i].state = AgentState(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                
                # handle q table
                table_spaces = ((c_float * 2) * 1024)() # Size
                self.agents[i].q_table = table_spaces
                for m in range(1024):
                    for n in range(2):
                        self.agents[i].q_table[m][n] = 0.0

                self.agents[i].exists = c_bool(False)


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
