import sys
import os
import json
from ctypes import *
#from gym_duckietown.dl_utils import *

def get_dl_turn_choice(choice):
    print(f"Printing choice {choice}")
    if choice == "Straight":
        return "STRAIGHT"
    if choice == "Left":
        return "LEFT"
    if choice == "Right":
        return "RIGHT"
    return choice

def get_dl_direction(direction):
    if direction == 'N':
        return 'NORTH'
    if direction == 'S':
        return 'SOUTH'
    if direction == 'E':
        return 'EAST'
    if direction == 'W':
        return 'WEST'
    return direction

# get the query blob from the query info
def get_query_blob(env, query_info):

    def get_model(q_table):
        c_q_table = []
        if q_table:
            for m in range(1024):
                c_q_table.append([float(q_table.qt[m][0]), float(q_table.qt[m][1])])
        else:
            for m in range(1024):
                for n in range(2):
                    c_q_table.append([0.0, 0.0])

        return c_q_table

    def get_environment(query_info):
        env_info = query_info['env_info']
        environment = {
            'intersection_x': env_info['intersection_x'],
            'intersection_z': env_info['intersection_z'],
            'robot_length': env_info['robot_length'],
            'grid_w': env_info['grid_w'],
            'grid_h': env_info['grid_h'],
            'road_tile_size': env_info['road_tile_size'],
            'max_steps': env_info['max_steps'],
            'num_agents': env_info['num_agents'],
            'model': get_model(env.agents[0].q_table),
        }
        return environment

    def get_agents(query_info):
        def get_agent(agent_info):

            def has_symbolic(counterfactuals, kind):
                for counterfactual in counterfactuals:
                    if counterfactual[kind]:
                        return True

                return False

            def sort_symbolics(counterfactuals):
                symbolics = {}
                symbolics['list_pos_x'] = []
                symbolics['list_pos_z'] = []
                symbolics['list_angle'] = []
                symbolics['list_forward_step'] = []
                symbolics['list_speed'] = []
                symbolics['list_signal_choice'] = []
                symbolics['list_turn_choice'] = []
                for counterfactual in counterfactuals:
                    if counterfactual['is_pos_x']:
                        symbolics['list_pos_x'].append(counterfactual)
                    if counterfactual['is_pos_z']:
                        symbolics['list_pos_z'].append(counterfactual)
                    if counterfactual['is_angle']:
                        symbolics['list_angle'].append(counterfactual)
                    if counterfactual['is_forward_step']:
                        symbolics['list_forward_step'].append(counterfactual)
                    if counterfactual['is_speed']:
                        symbolics['list_speed'].append(counterfactual)
                    if counterfactual['is_signalchoice']:
                        symbolics['list_signal_choice'].append(counterfactual)
                    if counterfactual['is_turnchoice']:
                        symbolics['list_turn_choice'].append(counterfactual)

                return symbolics

            symbolics = []
            for counterfactual in agent_info['counterfactuals']:
                symbolics.append(counterfactual)

            agent = {
                'concrete' : {
                    'id': agent_info['id'],
                    'agent_id': agent_info['agent_id'],
                    'pos_x': None if has_symbolic(agent_info['counterfactuals'], 'is_pos_x')
                        else agent_info['pos_x'],
                    'pos_z': None if has_symbolic(agent_info['counterfactuals'], 'is_pos_z')
                        else agent_info['pos_z'],
                    'angle': None if has_symbolic(agent_info['counterfactuals'], 'is_angle')
                        else agent_info['angle'],
                    'forward_step': None if has_symbolic(agent_info['counterfactuals'], 'is_forward_step')
                        else agent_info['forward_step'],
                    'speed': None if has_symbolic(agent_info['counterfactuals'], 'is_speed')
                        else agent_info['speed'],
                    'turn_choice': None if has_symbolic(agent_info['counterfactuals'], 'is_turnchoice')
                        else agent_info['turn_choice'],
                    'signal_choice': None if has_symbolic(agent_info['counterfactuals'], 'is_signalchoice')
                        else agent_info['signal_choice'],
                    'lookahead': agent_info['lookahead'],
                },

                'symbolic' : sort_symbolics(symbolics),

                'state' : {
                    'initial_direction': agent_info['initial_direction'],
                    'intersection_arrival': agent_info['intersection_arrival'],
                    'patience': agent_info['patience'],
                    'step_count': agent_info['step_count'],
                },
            }
            return agent

        agents_info = query_info['env_info']['agents']
        agents = {}
        for agent in agents_info:
            agents[agent['agent_id']] = get_agent(agent)


        return agents

    def get_log(query_info):
        agents_info = query_info['env_info']['agents'][0]['log']['agents']
        agents = {}
        for index, agent_info in list(enumerate(agents_info)):
            agents[f'agent{agents_info[index]}'] = {}
            agents[f'agent{agents_info[index]}']['pos_x'] = agent_info['pos_x']
            agents[f'agent{agents_info[index]}']['pos_z'] = agent_info['pos_z']
            agents[f'agent{agents_info[index]}']['angle'] = agent_info['angle']
            agents[f'agent{agents_info[index]}']['forward_step'] = agent_info['forward_step']
            agents[f'agent{agents_info[index]}']['signal_choice'] = agent_info['signal_choice']
            agents[f'agent{agents_info[index]}']['turn_choice'] = agent_info['turn_choice']
            agents[f'agent{agents_info[index]}']['lookahead'] = agent_info['lookahead']
            agents[f'agent{agents_info[index]}']['initial_direction'] = agent_info['initial_direction']
            agents[f'agent{agents_info[index]}']['intersection_arrival'] = agent_info['intersection_arrival']
            agents[f'agent{agents_info[index]}']['patience'] = agent_info['patience']
            agents[f'agent{agents_info[index]}']['step_count'] = agent_info['step_count']
        return agents


    def get_query(query_info):
        query = {
            'is_factual': query_info['query']['is_factual'] ,
            'is_existential': query_info['query']['is_existential'] ,
            'behavior': query_info['query']['behavior'] ,
        }
        return query

    # Print the json we are working with
    environment = get_environment(query_info)
    agents = get_agents(query_info)
    query = get_query(query_info)
    log = get_log(query_info)
    query_blob = {}
    query_blob['environment'] = environment
    query_blob['agents'] = dict(agents)
    query_blob['query'] = dict(query)
    query_blob['log'] = dict(log)
    json.dump(query_blob, open('src/webserver/soid_files/query_blobs/query_blob', 'w'), indent=2)

    return query_blob

# Generate the klee file
def generate_klee_file(query_blob):
    soidp = os.getenv('SOID_PATH')
    if not soidp:
        raise Exception('Unable to find soid to generate KLEE file')

    """
    This function will generate the klee file used by soid.

    """
    #query = json.loads(query_blob)
    query = query_blob
    klee_prefix = "src/webserver/soid_files/klee/"
    # open klee file
    klee_file = open((klee_prefix + "klee_file.c"), 'w', encoding="utf-8")
    # Imports
    klee_file.write("#include <string.h>\n")
    klee_file.write("#include \"../../../gym_duckietown/decision_logic/decision_logic.h\"\n\n")
    klee_file.write(f'#include \"{soidp}/soid/soidlib/soidlib.h\"\n')
    klee_file.write("int main(int argc, char **argv) {\n")

    environment = query["environment"]

    klee_file.write("    // Q table stuff\n")
    klee_file.write(f"   static float model[1024][2];\n")
    for m in range(1024):
        for n in range(2):
            klee_file.write(f"   model[{m}][{n}] = {environment['model'][m][n]};\n")


    # init env_info
    klee_file.write("    EnvironmentInfo info;\n")

    # Klee opent merge
    #klee_file.write("    klee_open_merge();\n")


    # Handle env information
    klee_file.write("\n    // Environment Information:\n")
    klee_file.write(f'    info.intersection_x = { environment["intersection_x"] };\n')
    klee_file.write(f'    info.intersection_z = { environment["intersection_z"] };\n')
    klee_file.write(f'    info.robot_length = { environment["robot_length"] };\n')
    klee_file.write(f'    info.grid_w = { environment["grid_w"] };\n')
    klee_file.write(f'    info.grid_h = { environment["grid_h"] };\n')
    klee_file.write(f'    info.road_tile_size = { environment["road_tile_size"] };\n')
    klee_file.write(f'    info.max_steps = { environment["max_steps"] };\n')
    klee_file.write(f'    info.num_agents = { environment["num_agents"] };\n')

    # Init agent array
    klee_file.write("\n    // Agent Array:\n")


    agents = query["agents"]
    # Initialize each agent
    for i in range(environment["num_agents"]):
        agent = agents[f'agent{i}']
        klee_file.write(f"\n    // Agent{i} Information:\n")
        klee_file.write(f'    info.agents[{i}].id = { agent["concrete"]["id"] };\n')
        # Position
        klee_file.write(f'    float agent{i}_pos_x, agent{i}_pos_z, agent{i}_angle, agent{i}_forward_step, agent{i}_speed, agent{i}_lookahead;\n')
        klee_file.write(f'    int agent{i}_signal_choice, agent{i}_turn_choice, agent{i}_initial_direction, agent{i}_intersection_arrival, agent{i}_step_count, agent{i}_patience;\n')

        klee_file.write(f'    klee_make_symbolic( &agent{i}_pos_x, sizeof(float), "agent{i}_pos_x");\n')
        klee_file.write(f'    klee_make_symbolic( &agent{i}_pos_z, sizeof(float), "agent{i}_pos_z");\n')

        #angle
        klee_file.write(f'    klee_make_symbolic( &agent{i}_angle, sizeof(float), "agent{i}_angle");\n')

        # Forward Step
        klee_file.write(f'    klee_make_symbolic( &agent{i}_forward_step, sizeof(float), "agent{i}_forward_step");\n')

        # Speed
        klee_file.write(f'    klee_make_symbolic( &agent{i}_speed, sizeof(float), "agent{i}_speed");\n')

        # Lookahead
        klee_file.write(f'    klee_make_symbolic( &agent{i}_lookahead, sizeof(float), "agent{i}_lookahead");\n')

        # signal_turn
        klee_file.write(f'    klee_make_symbolic( &agent{i}_signal_choice, sizeof(TurnChoice), "agent{i}_signal_choice");\n')
        klee_file.write(f'    klee_make_symbolic( &agent{i}_turn_choice, sizeof(TurnChoice), "agent{i}_turn_choice");\n')

        # Initial direction
        klee_file.write(f'    klee_make_symbolic( &agent{i}_initial_direction, sizeof(Direction), "agent{i}_initial_direction");\n')

        # Intersection_arrival
        klee_file.write(f'    klee_make_symbolic( &agent{i}_intersection_arrival, sizeof(int), "agent{i}_intersection_arrival");\n')

        # patience
        klee_file.write(f'    klee_make_symbolic( &agent{i}_patience, sizeof(int), "agent{i}_patience");\n')

        # Step count
        klee_file.write(f'    klee_make_symbolic( &agent{i}_step_count, sizeof(int), "agent{i}_step_count");\n')

        # If concrete is null, then we don't do this, as there will be a symbolic value.
        # concrete_pos_x
        if agent["concrete"]["pos_x"]:
            klee_file.write(f'    klee_assume( agent{i}_pos_x == (float) { agent["concrete"]["pos_x"] } ); // Concrete Val \n')

        # concrete_pos_z
        if agent["concrete"]["pos_z"]:
            klee_file.write(f'    klee_assume( agent{i}_pos_z == (float) { agent["concrete"]["pos_z"] } ); // Concrete Val \n')

        # concrete_angle
        if agent["concrete"]["angle"]:
            klee_file.write(f'    klee_assume( agent{i}_angle == (float) { agent["concrete"]["angle"] } ); // Concrete Val \n')

        # concrete_forward_Step
        if agent["concrete"]["forward_step"]:
            klee_file.write(f'    klee_assume( agent{i}_forward_step == (float) { agent["concrete"]["forward_step"] } ); // Concrete Val \n')

        # concrete_speed
        if agent["concrete"]["speed"]:
            klee_file.write(f'    klee_assume( agent{i}_speed == (float) { agent["concrete"]["speed"] } ); // Concrete Val \n')

        # concrete_signal_choice
        if agent["concrete"]["signal_choice"]:
            dl_value = get_dl_turn_choice(agent["concrete"]["signal_choice"])
            klee_file.write(f'    klee_assume( agent{i}_signal_choice == { dl_value } ); // Concrete Val \n')

        # concrete_turn_choice
        if agent["concrete"]["turn_choice"]:
            dl_value = get_dl_turn_choice(agent["concrete"]["turn_choice"])
            klee_file.write(f'    klee_assume( agent{i}_turn_choice == { dl_value } ); // Concrete Val \n')

        # Get stateful things
        # Lookhead
        klee_file.write(f'    klee_assume( agent{i}_lookahead == (float) { agent["concrete"]["lookahead"] }); // Concrete State Val \n')

        # intersection_arrival
        klee_file.write(f'    klee_assume( agent{i}_intersection_arrival == { agent["state"]["intersection_arrival"] }); // Concrete State Val \n')

        # initial_direction
        klee_file.write(f'    klee_assume( agent{i}_initial_direction == { get_dl_direction(agent["state"]["initial_direction"])}); // Concrete State Val \n')

        # patience
        klee_file.write(f'    klee_assume( agent{i}_patience == { agent["state"]["patience"] }); // Concrete State Val \n')

        # Stepcount
        klee_file.write(f'    klee_assume( agent{i}_step_count == { agent["state"]["step_count"] }); // Concrete State Val \n')

        # Handle the symbolic values pos_x
        for j in range(len(agent["symbolic"]["list_pos_x"])):
            counterfactual = agent["symbolic"]["list_pos_x"][j]
            # Symbolic_Pos x
            klee_file.write(f'    klee_assume( ')
            if counterfactual["is_value"]:
                klee_file.write(f'(agent{i}_pos_x  == (float) {counterfactual["value"]}) ')
            if counterfactual["is_range"]:
                klee_file.write(f'(agent{i}_pos_x >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_pos_x <= (float) {counterfactual["range"]["high_bound"]}) ')
            # if less than the last one, do disjunction
            if j < len(agent["symbolic"]["list_pos_x"]) - 1:
                klee_file.write(f'|| ')
            else:
                klee_file.write(f'); // Symbolic Values \n')

        # Handle the symbolic values pos_z
        for j in range(len(agent["symbolic"]["list_pos_z"])):
            counterfactual = agent["symbolic"]["list_pos_z"][j]
            # Symbolic_Pos x
            klee_file.write(f'    klee_assume( ')
            if counterfactual["is_value"]:
                klee_file.write(f'(agent{i}_pos_z  == (float) {counterfactual["value"]}) ')
            if counterfactual["is_range"]:
                klee_file.write(f'(agent{i}_pos_z >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_pos_z <= (float) {counterfactual["range"]["high_bound"]}) ')
            # if less than the last one, do disjunction
            if j < len(agent["symbolic"]["list_pos_z"]) - 1:
                klee_file.write(f'|| ')
            else:
                klee_file.write(f'); // Symbolic Values \n')

        # Handle the symbolic values angle
        for j in range(len(agent["symbolic"]["list_angle"])):
            counterfactual = agent["symbolic"]["list_angle"][j]
            # Symbolic_Pos x
            klee_file.write(f'    klee_assume( ')
            if counterfactual["is_value"]:
                klee_file.write(f'(agent{i}_angle  == (float) {counterfactual["value"]}) ')
            if counterfactual["is_range"]:
                klee_file.write(f'(agent{i}_angle >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_angle <= (float) {counterfactual["range"]["high_bound"]}) ')
            # if less than the last one, do disjunction
            if j < len(agent["symbolic"]["list_angle"]) - 1:
                klee_file.write(f'|| ')
            else:
                klee_file.write(f'); // Symbolic Values \n')

        # Handle the symbolic values forward_step
        for j in range(len(agent["symbolic"]["list_forward_step"])):
            counterfactual = agent["symbolic"]["list_forward_step"][j]
            # Symbolic_Pos x
            klee_file.write(f'    klee_assume( ')
            if counterfactual["is_value"]:
                klee_file.write(f'(agent{i}_forward_step  == (float) {counterfactual["value"]}) ')
            if counterfactual["is_range"]:
                klee_file.write(f'(agent{i}_forward_step >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_forward_step <= (float) {counterfactual["range"]["high_bound"]}) ')
            # if less than the last one, do disjunction
            if j < len(agent["symbolic"]["list_forward_step"]) - 1:
                klee_file.write(f'|| ')
            else:
                klee_file.write(f'); // Symbolic Values \n')

        # Handle the symbolic values speed
        for j in range(len(agent["symbolic"]["list_speed"])):
            counterfactual = agent["symbolic"]["list_speed"][j]
            # Symbolic_Pos x
            klee_file.write(f'    klee_assume( ')
            if counterfactual["is_value"]:
                klee_file.write(f'(agent{i}_speed  == (float) {counterfactual["value"]} )')
            if counterfactual["is_range"]:
                klee_file.write(f'(agent{i}_speed >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_speed <= (float) {counterfactual["range"]["high_bound"]}) ')
            # if less than the last one, do disjunction
            if j < len(agent["symbolic"]["list_speed"]) - 1:
                klee_file.write(f'|| ')
            else:
                klee_file.write(f'); // Symbolic Values \n')

        # Handle the symbolic values signal_choice
        for j in range(len(agent["symbolic"]["list_signal_choice"])):
            counterfactual = agent["symbolic"]["list_signal_choice"][j]
            # Symbolic_Pos x
            klee_file.write(f'    klee_assume( ')
            if counterfactual["is_value"]:
                klee_file.write(f'(agent{i}_signal_choice  == {counterfactual["value"]}) ')
            if counterfactual["is_range"]:
                klee_file.write(f'(agent{i}_signal_choice == ')
                for k in range(len(counterfactual["range"]["turn_choices"])):
                    if k == 0:
                        dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][0].upper())
                        klee_file.write(f' {dl_value}')
                    else:
                        dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][k].upper())
                        klee_file.write(f' || agent{i}_signal_choice == {dl_value}')
                klee_file.write(f')')

            # if less than the last one, do disjunction
            if j < len(agent["symbolic"]["list_signal_choice"]) - 1:
                klee_file.write(f'|| ')
            else:
                klee_file.write(f'); // Symbolic Values \n')

        # Handle the symbolic values turn_choice
        for j in range(len(agent["symbolic"]["list_turn_choice"])):
            counterfactual = agent["symbolic"]["list_turn_choice"][j]
            # Symbolic_Pos x
            klee_file.write(f'    klee_assume( ')
            if counterfactual["is_value"]:
                klee_file.write(f'(agent{i}_turn_choice  == {counterfactual["value"]}) ')
            if counterfactual["is_range"]:
                klee_file.write(f'(agent{i}_turn_choice == ')
                for k in range(len(counterfactual["range"]["turn_choices"])):
                    if k == 0:
                        dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][0].upper())
                        klee_file.write(f' {dl_value}')
                    else:
                        dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][k].upper())
                        klee_file.write(f' || agent{i}_turn_choice == {dl_value}')
            # if less than the last one, do disjunction
            if j < len(agent["symbolic"]["list_turn_choice"]) - 1:
                klee_file.write(f'|| ')
            else:
                klee_file.write(f'); // Symbolic Values \n')


        # Memcpy struct stuff
        # floats
        klee_file.write(f'    memmove( &info.agents[{i}].pos_x, &agent{i}_pos_x, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].pos_z, &agent{i}_pos_z, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].angle, &agent{i}_angle, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].forward_step, &agent{i}_forward_step, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].speed, &agent{i}_speed, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].lookahead, &agent{i}_lookahead, sizeof(float)); // Memcopy symb -> struct\n')
        # ints
        klee_file.write(f'    memmove( &info.agents[{i}].turn_choice, &agent{i}_turn_choice, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].signal_choice, &agent{i}_signal_choice, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].patience, &agent{i}_patience, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].intersection_arrival, &agent{i}_intersection_arrival, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].initial_direction, &agent{i}_initial_direction, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memmove( &info.agents[{i}].step_count, &agent{i}_step_count, sizeof(int)); // Memcopy symb -> struct\n')



        # Set the state for inferred variables
        # prev pos
    for i in range(environment["num_agents"]):
        klee_file.write(f'    float agent{i}_prev_pos_x, agent{i}_prev_pos_z, agent{i}_stop_x, agent{i}_stop_z;\n')

        klee_file.write(f'    int agent{i}_tile_x, agent{i}_tile_z, agent{i}_direction;\n')


        # Prev pos
        klee_file.write(f'    agent{i}_prev_pos_x = agent{i}_pos_x; // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].prev_pos_x, &agent{i}_prev_pos_x, sizeof(float)); // Memcopy symb -> struct\n\n')

        klee_file.write(f'    agent{i}_prev_pos_z = agent{i}_pos_z; // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].prev_pos_x, &agent{i}_prev_pos_x, sizeof(float)); // Memcopy symb -> struct\n\n')

        # direction
        klee_file.write(f'    agent{i}_direction = get_dl_direction(info.agents[{i}].angle/3.14*180); // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].direction, &agent{i}_direction, sizeof(int)); // Memcopy symb -> struct\n\n')

        # tile
        klee_file.write(f'    agent{i}_tile_x = get_tile_pos_x(agent{i}_pos_x, agent{i}_pos_z, info.road_tile_size); // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].tile_x, &agent{i}_tile_x, sizeof(int)); // Memcopy symb -> struct\n\n')

        klee_file.write(f'    agent{i}_tile_z = get_tile_pos_z(agent{i}_pos_x, agent{i}_pos_z, info.road_tile_size); // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].tile_z, &agent{i}_tile_z, sizeof(int)); // Memcopy symb -> struct\n\n')

        # stop pos
        klee_file.write(f'    agent{i}_stop_x = get_stop_pos_x(agent{i}_tile_x, agent{i}_tile_z, info.road_tile_size, agent{i}_direction, agent{i}_speed); // Calculated Variable\n');
        klee_file.write(f'    memmove( &info.agents[{i}].stop_x, &agent{i}_stop_x, sizeof(float)); // Memcopy symb -> struct\n\n')

        klee_file.write(f'    agent{i}_stop_z = get_stop_pos_z(agent{i}_tile_x, agent{i}_tile_z, info.road_tile_size, agent{i}_direction, agent{i}_speed); // Calculated Variable\n');
        klee_file.write(f'    memmove( &info.agents[{i}].stop_z, &agent{i}_stop_z, sizeof(float)); // Memcopy symb -> struct\n\n')

        # exists
        klee_file.write(f'    info.agents[{i}].exists = true; // exist \n\n')

        # Initialize states
        klee_file.write(f'    bool agent{i}_state_in_intersection, agent{i}_state_at_intersection_entry, agent{i}_state_intersection_empty, agent{i}_state_approaching_intersection, agent{i}_state_obj_in_range, agent{i}_state_has_right_of_way, agent{i}_state_safe_to_enter, agent{i}_state_cars_waiting_to_enter, agent{i}_state_car_entering_range, agent{i}_state_obj_behind_intersection, agent{i}_state_is_tailgating, agent{i}_state_next_to_go; \n')


        klee_file.write("\n     //Setting agent states\n")
        klee_file.write(f'    agent{i}_state_in_intersection = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_at_intersection_entry = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_intersection_empty = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_approaching_intersection = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_obj_in_range = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_has_right_of_way = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_safe_to_enter = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_cars_waiting_to_enter = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_car_entering_range = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_obj_behind_intersection = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_is_tailgating = false; //initial states\n')
        klee_file.write(f'    agent{i}_state_next_to_go = false; //initial states\n\n')

    # Copy out agent states
    klee_file.write("    // Copy out to agent states\n")
    # in_intersection
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // in_intersection\n")
        klee_file.write(f"    agent{i}_state_in_intersection = in_intersection(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.in_intersection, &agent{i}_state_in_intersection, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # at_intersection_entry
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // at_intersection_entry\n")
        klee_file.write(f"    agent{i}_state_at_intersection_entry = at_intersection_entry(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.at_intersection_entry, &agent{i}_state_at_intersection_entry, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # intersection_empty
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // intersection_empty\n")
        klee_file.write(f"    agent{i}_state_intersection_empty = intersection_empty(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.intersection_empty, &agent{i}_state_intersection_empty, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # approaching_intersection
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // approaching_intersection\n")
        klee_file.write(f"    agent{i}_state_approaching_intersection = approaching_intersection(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.approaching_intersection, &agent{i}_state_approaching_intersection, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # obj_in_range
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // obj_in_range\n")
        klee_file.write(f"    agent{i}_state_obj_in_range = object_in_range(&info, {i}, 1);\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.obj_in_range, &agent{i}_state_obj_in_range, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # right_of_way
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // right_of_way\n")
        klee_file.write(f"    agent{i}_state_has_right_of_way = has_right_of_way(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.has_right_of_way, &agent{i}_state_has_right_of_way, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # next_to_go
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // next_to_go\n")
        klee_file.write(f"    agent{i}_state_next_to_go = next_to_go(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.next_to_go, &agent{i}_state_next_to_go, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # safe_to_enter
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // safe_to_enter\n")
        klee_file.write(f"    agent{i}_state_safe_to_enter = safe_to_enter(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.safe_to_enter, &agent{i}_state_safe_to_enter, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # cars_waiting_to_enter
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // cars_waiting_to_enter\n")
        klee_file.write(f"    agent{i}_state_cars_waiting_to_enter = cars_waiting_to_enter(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.cars_waiting_to_enter, &agent{i}_state_cars_waiting_to_enter, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # car_entering_range
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // car_entering_range\n")
        klee_file.write(f"    agent{i}_state_car_entering_range = car_entering_range(&info, {i}, 1);\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.car_entering_range, &agent{i}_state_car_entering_range, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # obj_behind_intersection
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // obj_behind_intersection\n")
        klee_file.write(f"    agent{i}_state_obj_behind_intersection = object_in_range(&info, {i}, 2);\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.obj_behind_intersection, &agent{i}_state_obj_behind_intersection, sizeof(bool)); // Memcopy symb -> struct\n\n')

    # tailgating
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // is_tailgating\n")
        klee_file.write(f"    agent{i}_state_is_tailgating = is_tailgating(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.is_tailgating, &agent{i}_state_is_tailgating, sizeof(bool)); // Memcopy symb -> struct\n\n')




    #klee_file.write(f'    // Klee Close Merge();\n')
    #klee_file.write(f'    klee_close_merge();\n')

    # handle the q table nd proceed model ONLY FOR AGENT 0
    agent = agents['agent0']


    # Get learning state row
    klee_file.write("\n    // Learning Row\n")
    klee_file.write("    int mrow;\n")
    klee_file.write("    mrow = get_learning_state(&info, 0);\n")

    klee_file.write("\n    // Invoke proceed\n")

    klee_file.write(f'    bool will_proceed, __soid__will_proceed;\n')
    klee_file.write(f'    klee_make_symbolic( &__soid__will_proceed, sizeof(bool), "__soid__will_proceed");\n')
    klee_file.write("    will_proceed = proceed_model(model, mrow);\n")
    #klee_file.write("    will_proceed = proceed_good_agent(&info, mrow);\n")
    klee_file.write(f'    klee_assume( will_proceed == __soid__will_proceed);\n')

    klee_file.write("}\n")

    klee_file.close()

    #makefile
    makefile = open((klee_prefix + "makefile"),'w', encoding="utf-8")

    makefile.write(f'cc={soidp}/llvm-project/release/bin/clang -std=c99\n')
    makefile.write(f'opt={soidp}/llvm-project/release/bin/opt\n')
    makefile.write(f'link={soidp}/llvm-project/release/bin/llvm-link\n')

    # Inbetween files
    makefile.write("BC1=./inter1.bc\n\n")
    makefile.write("BC2=./inter2.bc\n\n")
    makefile.write("BC3=./inter3.bc\n\n")
    makefile.write("BC=./inter.bc\n\n")

    # Paths
    makefile.write(f'KLEE={soidp}/klee-float/include/klee\n')
    makefile.write(f'KEXEC={soidp}/klee-float/build/bin/klee\n')
    makefile.write(f'PRE-LIB-KLEE=-L {soidp}/klee-float/build/lib/\n')
    makefile.write("POST-LIB-KLEE=-lkleeRuntest\n\n")
    makefile.write(f'SOIDLIB={soidp}/soid/soidlib\n\n')
    makefile.write("symbolic:\n")

    # Compile types.c
    makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ../../../gym_duckietown/decision_logic/types.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC1)\n")

    # Compile decision_logic.c
    makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ../../../gym_duckietown/decision_logic/decision_logic.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC2)\n")

    # Compile klee_file.c
    makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ./klee_file.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC3)\n")
    #makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ./klee_file.c -o $(BC)\n")

    # link
    makefile.write("	$(link) $(BC1) $(BC2) $(BC3) -o $(BC) \n")
    #makefile.write("	$(link) $(BC2) $(BC3) -o $(BC) \n")

    # exec klee
    makefile.write("	$(KEXEC) -silent-klee-assume -write-smt2s -use-merge $(BC)\n")


    makefile.write("\nclean:\n")
    makefile.write("	rm -f ./inter1.bc\n")
    makefile.write("	rm -f ./inter2.bc\n")
    makefile.write("	rm -f ./inter3.bc\n")
    makefile.write("	rm -f ./inter.bc\n")
    makefile.write("	rm -rf ./klee-out-*\n")
    makefile.write("	rm -rf ./klee-last\n")

    makefile.close()


    # print(agents)
    # return file_descriptor, file_path
    return None


if __name__ == '__main__':
    query_prefix = 'src/webserver/soid_files/query_blobs/experiments/'
    query_blob = json.load(open(query_prefix + sys.argv[1]))
    generate_klee_file(query_blob)
