import sys
import os
import json
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
        }
        return environment

    def get_agents(query_info):
        def get_agent(agent_info):
            
            def has_symbolic(counterfactuals, kind):
                for counterfactual in counterfactuals:
                    if counterfactual[kind]:
                        return True

                return False


            symbolic = []
            for counterfactual in agent_info['counterfactuals']:
                symbolic.append(counterfactual)

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
                'symbolic' : symbolic,
                'state' : {
                    'initial_direction': agent_info['initial_direction'],
                    'intersection_arrival': agent_info['intersection_arrival'],
                    'patience': agent_info['patience'],
                    'step_count': agent_info['step_count'],
                    'turn_choice': agent_info['turn_choice'],
                    'signal_choice': agent_info['signal_choice'],
                    'q_table': agent_info['q_table'],
                },
            }
            return agent

        agents_info = query_info['env_info']['agents']
        agents = {}
        for agent in agents_info:
            agents[agent['agent_id']] = get_agent(agent)

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
    query_blob = {}
    query_blob['environment'] = environment
    query_blob['agents'] = dict(agents)
    query_blob['query'] = dict(query)
    json.dump(query_blob, open('src/webserver/soid_files/query_blobs/query_blob', 'w'))

    return query_blob

# Generate the klee file
def generate_klee_file(query_blob):
    """
    This function will generate the klee file used by soid. 

    """
    #query = json.loads(query_blob)
    query = query_blob
    klee_prefix = "src/webserver/soid_files/klee/"
    # open klee file
    klee_file = open((klee_prefix + "klee_file.c"), 'w', encoding="utf-8")
    # Imports
    klee_file.write("#include \"/tools/soid/soid/soid/soidlib/soidlib.h\"\n")
    klee_file.write("#include \"../../../gym_duckietown/decision_logic/decision_logic.c\"\n\n")
    klee_file.write("int main(int argc, char **argv) {\n")
    
    # init env_info
    klee_file.write("    EnvironmentInfo *info = malloc(sizeof(EnvironmentInfo));\n")
    
    # Klee opent merge
    klee_file.write("    klee_open_merge();\n")

    environment = query["environment"]
    
    # Handle env information
    klee_file.write("\n    // Environment Information:\n")
    klee_file.write(f'    info->intersection_x = { environment["intersection_x"] };\n')
    klee_file.write(f'    info->intersection_z = { environment["intersection_z"] };\n')
    klee_file.write(f'    info->robot_length = { environment["robot_length"] };\n')
    klee_file.write(f'    info->grid_w = { environment["grid_w"] };\n')
    klee_file.write(f'    info->grid_h = { environment["grid_h"] };\n')
    klee_file.write(f'    info->road_tile_size = { environment["road_tile_size"] };\n')
    klee_file.write(f'    info->max_steps = { environment["max_steps"] };\n')
    
    # Init agent array
    klee_file.write("\n    // Agent Array:\n")
    klee_file.write(f'    EnvironmentAgentArray *agents = malloc(sizeof(EnvironmentAgentArray));\n')
    klee_file.write(f"    agents->num_agents = {environment['num_agents']};")
    klee_file.write("    info->agents = *agents;")

    
    agents = query["agents"]
    # Initialize each agent
    for i in range(environment["num_agents"]):
        agent = agents[f'agent{i}']
        klee_file.write(f"\n    // Agent{i} Information:\n")
        klee_file.write(f'    EnvironmentAgent agent{i} = agents->agents_array[{i}];\n')
        klee_file.write(f'    agent{i}.id = { agent["concrete"]["id"] };\n')
        # Position
        klee_file.write(f'    float agent{i}_pos_x, agent{i}_pos_z, agent{i}_angle, agent{i}_forward_step, agent{i}_speed, agent{i}_lookahead;\n')
        klee_file.write(f'    int agent{i}_signal_choice, agent{i}_turn_choice, agent{i}_initial_direction, agent{i}_intersection_arrival, agent{i}_step_count, agent{i}_patience;\n')

        klee_file.write(f'    klee_make_symbolic( &agent{i}_pos_x, sizeof(float), "agent{i}_pos_x");\n')
        klee_file.write(f'    klee_make_symbolic( &agent{i}_pos_z, sizeof(float), "agent{i}_pos_z");\n')
        
        #angle
        klee_file.write(f'    klee_make_symbolic( &agent{i}_angle, sizeof(float), "agent{i}_angle");\n')
        
        # Forward Step
        klee_file.write(f'    klee_make_symbolic( &agent{i}_forward_step, sizeof(float), "agent{i}_forward_step");\n')
        
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
            klee_file.write(f'    klee_assume( agent{i}_pos_x == { agent["concrete"]["pos_x"] } ); // Concrete Val \n')

        # concrete_pos_z
        if agent["concrete"]["pos_z"]:
            klee_file.write(f'    klee_assume( agent{i}_pos_z == { agent["concrete"]["pos_z"] } ); // Concrete Val \n') 

        # concrete_angle
        if agent["concrete"]["angle"]:
            klee_file.write(f'    klee_assume( agent{i}_angle == { agent["concrete"]["angle"] } ); // Concrete Val \n')

        # concrete_forward_Step
        if agent["concrete"]["forward_step"]:
            klee_file.write(f'    klee_assume( agent{i}_forward_step == { agent["concrete"]["forward_step"] } ); // Concrete Val \n')

        # concrete_speed
        if agent["concrete"]["speed"]:
            klee_file.write(f'    klee_assume( agent{i}_speed == { agent["concrete"]["speed"] } ); // Concrete Val \n')

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
        klee_file.write(f'    klee_assume( agent{i}_lookahead == { agent["concrete"]["lookahead"] }); // Concrete State Val \n')
        
        # intersection_arrival
        klee_file.write(f'    klee_assume( agent{i}_intersection_arrival == { agent["state"]["intersection_arrival"] }); // Concrete State Val \n')

        # initial_direction
        klee_file.write(f'    klee_assume( agent{i}_initial_direction == { get_dl_direction(agent["state"]["initial_direction"])}); // Concrete State Val \n')

        # patience
        klee_file.write(f'    klee_assume( agent{i}_patience == { agent["state"]["patience"] }); // Concrete State Val \n')
        
        # Stepcount
        klee_file.write(f'    klee_assume( agent{i}_step_count == { agent["state"]["step_count"] }); // Concrete State Val \n')

        # Handle the symbolic values
        for j in range(len(agent["symbolic"])):
            counterfactual = agent["symbolic"][j]
            # Symbolic_Pos x
            if counterfactual["is_pos_x"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_x == {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_x >= {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}.pos_x <= {counterfactual["range"]["high_bound"]}); // Symbolic Range\n')

            # Symbolic_Pos z
            if counterfactual["is_pos_z"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_z == {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_z >= {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}.pos_z <= {counterfactual["range"]["high_bound"]}); // Symbolic Range\n') 

            # Symbolic_Angle
            if counterfactual["is_angle"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_angle == {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_angle >= {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_angle <= {counterfactual["range"]["high_bound"]}); // Symbolic Range\n')   

            # Symbolic_forward_step
            if counterfactual["is_forward_step"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_is_forward_step == {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_is_forward_step >= {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_is_forward_step <= {counterfactual["range"]["high_bound"]}); // Symbolic Range\n')

            # Symbolic_speed
            if counterfactual["is_speed"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_speed == {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_speed >= {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_speed <= {counterfactual["range"]["high_bound"]});\n')

            # Symbolic_signal_choice
            if counterfactual["is_signalchoice"]:
                if counterfactual["is_value"]:
                    dl_value = get_dl_turn_choice(counterfactual['value'].upper())
                    klee_file.write(f'    klee_assume( agent{i}_signal_choice == {dl_value} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_signal_choice ==')
                    for k in range(len(counterfactual["range"]["turn_choices"])):
                        if k == 0:
                            dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][0].upper())
                            klee_file.write(f' {dl_value}')
                        else:
                            dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][k].upper())
                            klee_file.write(f' || agent{i}_signal_choice == {dl_value}')
                    klee_file.write("); // Symbolic Range\n")

            # Symbolic_turn_choice
            if counterfactual["is_turnchoice"]:
                if counterfactual["is_value"]:
                    dl_value = get_dl_turn_choice(counterfactual['value'].upper())
                    klee_file.write(f'    klee_assume( agent{i}_turn_choice == {dl_value} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_turn_choice ==')
                    for k in range(len(counterfactual["range"]["turn_choices"])):
                        if k == 0:
                            dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][0].upper())
                            klee_file.write(f' {dl_value}')
                        else:
                            dl_value = get_dl_turn_choice(counterfactual['range']['turn_choices'][k].upper())
                            klee_file.write(f' || agent{i}_turn_choice == {dl_value}')
                    klee_file.write("); // Symbolic Range\n")

        # Memcpy struct stuff
        # floats
        klee_file.write(f'    memcpy( &agent{i}.prev_pos_x, &agent{i}_pos_x, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.prev_pos_z, &agent{i}_pos_z, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.angle, &agent{i}_angle, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.forward_step, &agent{i}_forward_step, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.speed, &agent{i}_speed, sizeof(float)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.lookahead, &agent{i}_lookahead, sizeof(float)); // Memcopy symb -> struct\n')
        # ints
        klee_file.write(f'    memcpy( &agent{i}.turn_choice, &agent{i}_turn_choice, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.signal_choice, &agent{i}_signal_choice, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.patience, &agent{i}_patience, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.intersection_arrival, &agent{i}_intersection_arrival, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.initial_direction, &agent{i}_initial_direction, sizeof(int)); // Memcopy symb -> struct\n')
        klee_file.write(f'    memcpy( &agent{i}.step_count, &agent{i}_step_count, sizeof(int)); // Memcopy symb -> struct\n')

        # Seet the state for inferred variables
        # prev pos
        klee_file.write(f'    agent{i}.prev_pos_z = agent{i}.pos_x; // Calculated Variable\n')
        klee_file.write(f'    agent{i}.prev_pos_z = agent{i}.pos_z; // Calculated Variable\n')
        
        # direction
        klee_file.write(f'    agent{i}.direction = get_direction(agent{i}.angle/3.14*180); // Calculated Variable\n')
        
        # tile pos
        klee_file.write(f'    TilePos *agent{i}_tile_pos = get_tile_pos(agent{i}.pos_x, agent{i}.pos_z, info->road_tile_size); // Calculated Variable\n')
        klee_file.write(f'    agent{i}.tile_x = agent{i}_tile_pos->x; // Calculated Variable\n')
        klee_file.write(f'    agent{i}.tile_z = agent{i}_tile_pos->z; // Calculated Variable\n')
        
        # stop pos
        klee_file.write(f'    StopPos *agent{i}_stop_pos = get_stop_pos(agent{i}.tile_x, agent{i}.tile_z, info->road_tile_size, agent{i}.direction, agent{i}.speed); // Calculated Variable\n')
        klee_file.write(f'    agent{i}.stop_x = agent{i}_stop_pos->x; // Calculated Variable\n')
        klee_file.write(f'    agent{i}.stop_z = agent{i}_stop_pos->z; // Calculated Variable\n')

        # Initialize states
        klee_file.write(f'    agent{i}.exists = true; // exist \n\n')
        klee_file.write(f'    agent{i}.state.in_intersection = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.at_intersection_entry = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.intersection_empty = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.approaching_intersection = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.obj_in_range = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.has_right_of_way = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.safe_to_enter = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.cars_waiting_to_enter = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.car_entering_range = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.obj_behind_intersection = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.is_tailgating = false; //initial states\n')
        klee_file.write(f'    agent{i}.state.next_to_go = false; //initial states\n\n')
        
    klee_file.write("\n     //Setting agent states\n")

    # in_intersection
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.in_intersection = in_intersection(info, i);\n")
    klee_file.write("     }\n")

    # at_intersection_entry
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.at_intersection_entry = at_intersection_entry(info, i);\n")
    klee_file.write("     }\n")

    # intersection_empty
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.intersection_empty = intersection_empty(info, i);\n")
    klee_file.write("     }\n")

    # approaching intersection
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.approaching_intersection = approaching_intersection(info, i);\n")
    klee_file.write("     }\n")

    # obj_in_range
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.obj_in_range = object_in_range(info, i, 1);\n")
    klee_file.write("     }\n")

    # Right of way
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.has_right_of_way = has_right_of_way(info, i);\n")
    klee_file.write("     }\n")

    # Next to go
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.next_to_go = next_to_go(info, i);\n")
    klee_file.write("     }\n")

    # safe_to_enter
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.safe_to_enter = safe_to_enter(info, i);\n")
    klee_file.write("     }\n")

    # cars_waiting_to_enter
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.cars_waiting_to_enter = cars_waiting_to_enter(info, i);\n")
    klee_file.write("     }\n")

    # car_entering_range
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.car_entering_range = car_entering_range(info, i, 1);\n")
    klee_file.write("     }\n")

    # obj_behind_intersection
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.obj_behind_intersection = car_entering_range(info, i, 1);\n")
    klee_file.write("     }\n")

    # tailgating
    klee_file.write("    for(int i = 0; i < agents->num_agents; i++){\n")
    klee_file.write("        agents->agents_array[i].state.is_tailgating = is_tailgating(info, i);\n")
    klee_file.write("     }\n")

    
    # handle the q table nd proceed model ONLY FOR AGENT 0
    klee_file.write("    // Q table stuff\n")
    
    agent = agents['agent0']
    for m in range(1024):
        for n in range(2):
            klee_file.write(f"   info->agents.agents_array[{i}].q_table[{m}][{n}] = {agent['state']['q_table'][m][n]};\n")


    # Get learning state row
    klee_file.write("\n    // Learning Row\n")
    klee_file.write("    int mrow = get_learning_state(info, 0);\n")

    klee_file.write("\n    // Invoke proceed\n")
    
    klee_file.write(f'    bool will_proceed;\n')
    klee_file.write(f'    klee_make_symbolic( &will_proceed, sizeof(bool), "will_proceed");\n')
    klee_file.write("    will_proceed = proceed_model(agents->agents_array[0].q_table, mrow);\n")



    
    klee_file.write("}\n")
    
    klee_file.close()
    
    #makefile
    makefile = open((klee_prefix + "makefile"),'w', encoding="utf-8")
    
    makefile.write("cc=/tools/soid/soid/llvm-project/release/bin/clang -std=c99\n")
    makefile.write("opt=/tools/soid/soid/llvm-project/release/bin/opt\n")
    makefile.write("link=/tools/soid/soid/llvm-project/release/bin/llvm-link\n")

    # Inbetween files
    #makefile.write("BC1=./inter1.bc\n\n")
    #makefile.write("BC2=./inter2.bc\n\n")
    #makefile.write("BC3=./inter3.bc\n\n")
    makefile.write("BC=./inter.bc\n\n")
    
    # Paths
    makefile.write("KLEE=/tools/soid/soid/klee-float/include/klee\n")
    makefile.write("KEXEC=/tools/soid/soid/klee-float/build/bin/klee\n")
    makefile.write("PRE-LIB-KLEE=-L /tools/soid/soid/klee-float/build/lib/\n")
    makefile.write("POST-LIB-KLEE=-lkleeRuntest\n\n")
    makefile.write("SOIDLIB=/tools/soid/soid/soid/soidlib\n\n")
    makefile.write("symbolic:\n")
    
    # Compile types.c
    #makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 /home/mje48/duckietown-soid/src/gym_duckietown/decision_logic/types.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC1)\n")

    # Compile decision_logic.c
    #makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 /home/mje48/duckietown-soid/src/gym_duckietown/decision_logic/decision_logic.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC2)\n")

    # Compile klee_file.c
    #makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ./klee_file.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC3)\n")
    makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ./klee_file.c -o $(BC)\n")
    
    # link
    #makefile.write("	$(link) $(BC1) $(BC2) $(BC2) -o $(BC) \n")

    # exec klee
    makefile.write("	$(KEXEC) -silent-klee-assume -write-smt2s -use-merge $(BC)\n")

    
    makefile.write("\nclean:\n")
    makefile.write("	rm -f ./inter.bc\n")
    makefile.write("	rm -rf ./klee-out-*\n")
    makefile.write("	rm -rf ./klee-last\n")
    
    makefile.close()
    
    
    # print(agents)
    # return file_descriptor, file_path
    return None


if __name__ == '__main__':
    query_blob = json.load(open('src/webserver/soid_files/query_blobs/query_blob'))
    generate_klee_file(query_blob)