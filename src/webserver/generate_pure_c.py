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

# Generate the klee file
def generate_klee_file(query_blob):
    """
    This function will generate the klee file used by soid. 

    """
    #query = json.loads(query_blob)
    query = query_blob
    klee_prefix = "src/webserver/soid_files/c-debug"
    # open klee file
    klee_file = open((klee_prefix + "pure.c"), 'w', encoding="utf-8")
    # Imports
    klee_file.write("#include <string.h>\n")
    klee_file.write("#include <stdio.h>\n")
    klee_file.write("#include \"../../../gym_duckietown/decision_logic/decision_logic.h\"\n\n")
    klee_file.write("int main(int argc, char **argv) {\n")
    
    # init env_info
    klee_file.write("    EnvironmentInfo info;\n")
    
    environment = query["environment"]
    
    # Handle env information
    klee_file.write("\n    // Environment Information:\n")
    klee_file.write(f'    info.intersection_x = { environment["intersection_x"] };\n')
    klee_file.write(f'    printf("info.intersection_x %d\\n", info.intersection_x );\n')
    klee_file.write(f'    info.intersection_z = { environment["intersection_z"] };\n')
    klee_file.write(f'    printf("info.intersection_z %d\\n", info.intersection_z );\n')

    klee_file.write(f'    info.robot_length = { environment["robot_length"] };\n')
    klee_file.write(f'    printf("info.robot_length %f\\n", info.robot_length );\n')

    klee_file.write(f'    info.grid_w = { environment["grid_w"] };\n')
    klee_file.write(f'    printf("info.grid_w %d\\n", info.grid_w );\n')
    klee_file.write(f'    info.grid_h = { environment["grid_h"] };\n')
    klee_file.write(f'    printf("info.grid_h %d\\n", info.grid_h );\n')

    klee_file.write(f'    info.road_tile_size = { environment["road_tile_size"] };\n')
    klee_file.write(f'    printf("info.road_tile_size %f\\n", info.road_tile_size );\n')
    

    klee_file.write(f'    info.max_steps = { environment["max_steps"] };\n')
    klee_file.write(f'    printf("info.max_steps %d\\n", info.max_steps );\n')
    
    klee_file.write(f'    info.num_agents = { environment["num_agents"] };\n')
    klee_file.write(f'    printf("info.num_agents %d\\n", info.num_agents );\n\n')

    
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

        # Handle the symbolic values
        for j in range(len(agent["symbolic"])):
            counterfactual = agent["symbolic"][j]
            # Symbolic_Pos x
            if counterfactual["is_pos_x"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_x == (float) {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_x >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}.pos_x <= (float) {counterfactual["range"]["high_bound"]}); // Symbolic Range\n')

            # Symbolic_Pos z
            if counterfactual["is_pos_z"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_z == (float) {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_pos_z >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}.pos_z <= (float) {counterfactual["range"]["high_bound"]}); // Symbolic Range\n') 

            # Symbolic_Angle
            if counterfactual["is_angle"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_angle == (float) {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_angle >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_angle <= (float) {counterfactual["range"]["high_bound"]}); // Symbolic Range\n')   

            # Symbolic_forward_step
            if counterfactual["is_forward_step"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_is_forward_step == (float) {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_is_forward_step >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_is_forward_step <= (float) {counterfactual["range"]["high_bound"]}); // Symbolic Range\n')

            # Symbolic_speed
            if counterfactual["is_speed"]:
                if counterfactual["is_value"]:
                    klee_file.write(f'    klee_assume( agent{i}_speed == (float) {counterfactual["value"]} ); // Symbolic Value\n')
                elif counterfactual["is_range"]:
                    klee_file.write(f'    klee_assume( agent{i}_speed >= (float) {counterfactual["range"]["low_bound"]} && '
                    f'agent{i}_speed <= (float) {counterfactual["range"]["high_bound"]});\n')

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
        klee_file.write(f'    float __soid__agent{i}_prev_pos_x, __soid__agent{i}_prev_pos_z, __soid__agent{i}_stop_x, __soid__agent{i}_stop_z;\n\n')

        klee_file.write(f'    int agent{i}_tile_x, agent{i}_tile_z, agent{i}_direction;\n')
        klee_file.write(f'    int __soid__agent{i}_tile_x, __soid__agent{i}_tile_z, __soid__agent{i}_direction;\n')


        
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_prev_pos_x, sizeof(float), "__soid__agent{i}_prev_pos_x");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_prev_pos_z, sizeof(float), "__soid__agent{i}_prev_pos_z");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_stop_x, sizeof(float), "__soid__agent{i}_stop_x");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_stop_z, sizeof(float), "__soid__agent{i}_stop_z");\n\n')

        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_tile_x, sizeof(int), "__soid__agent{i}_tile_x");\n\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_tile_z, sizeof(int), "__soid__agent{i}_tile_z");\n\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_direction, sizeof(int), "__soid__agent{i}_direction");\n\n')
        
        # Prev pos
        klee_file.write(f'    agent{i}_prev_pos_x = agent{i}_pos_x; // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].prev_pos_x, &agent{i}_prev_pos_x, sizeof(float)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_prev_pos_x == __soid__agent{i}_prev_pos_x);\n')
        
        klee_file.write(f'    agent{i}_prev_pos_z = agent{i}_pos_z; // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].prev_pos_x, &agent{i}_prev_pos_x, sizeof(float)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_prev_pos_x == __soid__agent{i}_prev_pos_x);\n')

        # direction
        klee_file.write(f'    agent{i}_direction = get_dl_direction(info.agents[{i}].angle/3.14*180); // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].direction, &agent{i}_direction, sizeof(int)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_direction == __soid__agent{i}_direction);\n')
        
        # tile 
        klee_file.write(f'    agent{i}_tile_x = get_tile_pos_x(agent{i}_pos_x, agent{i}_pos_z, info.road_tile_size); // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].tile_x, &agent{i}_tile_x, sizeof(int)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_tile_x == __soid__agent{i}_tile_x);\n')

        klee_file.write(f'    agent{i}_tile_z = get_tile_pos_z(agent{i}_pos_x, agent{i}_pos_z, info.road_tile_size); // Calculated Variable\n')
        klee_file.write(f'    memmove( &info.agents[{i}].tile_z, &agent{i}_tile_z, sizeof(int)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_tile_z == __soid__agent{i}_tile_z);\n')
        
        # stop pos
        klee_file.write(f'    agent{i}_stop_x = get_stop_pos_x(agent{i}_tile_x, agent{i}_tile_z, info.road_tile_size, agent{i}_direction, agent{i}_speed); // Calculated Variable\n'); 
        klee_file.write(f'    memmove( &info.agents[{i}].stop_x, &agent{i}_stop_x, sizeof(float)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_stop_x == __soid__agent{i}_stop_x);\n')

        klee_file.write(f'    agent{i}_stop_z = get_stop_pos_z(agent{i}_tile_x, agent{i}_tile_z, info.road_tile_size, agent{i}_direction, agent{i}_speed); // Calculated Variable\n'); 
        klee_file.write(f'    memmove( &info.agents[{i}].stop_z, &agent{i}_stop_z, sizeof(float)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_stop_z == __soid__agent{i}_stop_z);\n')
        
        # exists
        klee_file.write(f'    info.agents[{i}].exists = true; // exist \n\n')

        # Initialize states
        klee_file.write(f'    bool agent{i}_state_in_intersection, agent{i}_state_at_intersection_entry, agent{i}_state_intersection_empty, agent{i}_state_approaching_intersection, agent{i}_state_obj_in_range, agent{i}_state_has_right_of_way, agent{i}_state_safe_to_enter, agent{i}_state_cars_waiting_to_enter, agent{i}_state_car_entering_range, agent{i}_state_obj_behind_intersection, agent{i}_state_is_tailgating, agent{i}_state_next_to_go; \n')

        klee_file.write(f'    bool __soid__agent{i}_state_in_intersection, __soid__agent{i}_state_at_intersection_entry, __soid__agent{i}_state_intersection_empty, __soid__agent{i}_state_approaching_intersection, __soid__agent{i}_state_obj_in_range, __soid__agent{i}_state_has_right_of_way, __soid__agent{i}_state_safe_to_enter, __soid__agent{i}_state_cars_waiting_to_enter, __soid__agent{i}_state_car_entering_range, __soid__agent{i}_state_obj_behind_intersection, __soid__agent{i}_state_is_tailgating, __soid__agent{i}_state_next_to_go; \n')

        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_in_intersection, sizeof(bool), "__soid__agent{i}_state_in_intersection");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_at_intersection_entry, sizeof(bool), "__soid__agent{i}_state_at_intersection_entry");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_intersection_empty, sizeof(bool), "__soid__agent{i}_state_intersection_empty");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_approaching_intersection, sizeof(bool), "__soid__agent{i}_state_approaching_intersection");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_obj_in_range, sizeof(bool), "__soid__agent{i}_state_obj_in_range");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_has_right_of_way, sizeof(bool), "__soid__agent{i}_state_has_right_of_way");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_safe_to_enter, sizeof(bool), "__soid__agent{i}_state_safe_to_enter");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_cars_waiting_to_enter, sizeof(bool), "__soid__agent{i}_state_cars_waiting_to_enter");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_car_entering_range, sizeof(bool), "__soid__agent{i}_state_car_entering_range");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_obj_behind_intersection, sizeof(bool), "__soid__agent{i}_state_obj_behind_intersection");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_is_tailgating, sizeof(bool), "__soid__agent{i}_state_is_tailgating");\n')
        klee_file.write(f'    klee_make_symbolic( &__soid__agent{i}_state_next_to_go, sizeof(bool), "__soid__agent{i}_state_next_to_go");\n')

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
        klee_file.write(f'    klee_assume( agent{i}_state_in_intersection == __soid__agent{i}_state_in_intersection);\n')

    # at_intersection_entry
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // at_intersection_entry\n")
        klee_file.write(f"    agent{i}_state_at_intersection_entry = at_intersection_entry(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.at_intersection_entry, &agent{i}_state_at_intersection_entry, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_at_intersection_entry == __soid__agent{i}_state_at_intersection_entry);\n')

    # intersection_empty
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // intersection_empty\n")
        klee_file.write(f"    agent{i}_state_intersection_empty = intersection_empty(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.intersection_empty, &agent{i}_state_intersection_empty, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_intersection_empty == __soid__agent{i}_state_intersection_empty);\n')

    # approaching_intersection
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // approaching_intersection\n")
        klee_file.write(f"    agent{i}_state_approaching_intersection = approaching_intersection(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.approaching_intersection, &agent{i}_state_approaching_intersection, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_approaching_intersection == __soid__agent{i}_state_approaching_intersection);\n')

    # obj_in_range
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // obj_in_range\n")
        klee_file.write(f"    agent{i}_state_obj_in_range = object_in_range(&info, {i}, 1);\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.obj_in_range, &agent{i}_state_obj_in_range, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_obj_in_range == __soid__agent{i}_state_obj_in_range);\n')

    # right_of_way
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // right_of_way\n")
        klee_file.write(f"    agent{i}_state_has_right_of_way = has_right_of_way(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.has_right_of_way, &agent{i}_state_has_right_of_way, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_has_right_of_way == __soid__agent{i}_state_has_right_of_way);\n')

    # next_to_go
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // next_to_go\n")
        klee_file.write(f"    agent{i}_state_next_to_go = next_to_go(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.next_to_go, &agent{i}_state_next_to_go, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_next_to_go == __soid__agent{i}_state_next_to_go);\n')

    # safe_to_enter
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // safe_to_enter\n")
        klee_file.write(f"    agent{i}_state_safe_to_enter = safe_to_enter(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.safe_to_enter, &agent{i}_state_safe_to_enter, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_safe_to_enter == __soid__agent{i}_state_safe_to_enter);\n')

    # cars_waiting_to_enter
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // cars_waiting_to_enter\n")
        klee_file.write(f"    agent{i}_state_cars_waiting_to_enter = cars_waiting_to_enter(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.cars_waiting_to_enter, &agent{i}_state_cars_waiting_to_enter, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_cars_waiting_to_enter == __soid__agent{i}_state_cars_waiting_to_enter);\n')

    # car_entering_range
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // car_entering_range\n")
        klee_file.write(f"    agent{i}_state_car_entering_range = car_entering_range(&info, {i}, 1);\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.car_entering_range, &agent{i}_state_car_entering_range, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_car_entering_range == __soid__agent{i}_state_car_entering_range);\n')

    # obj_behind_intersection
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // obj_behind_intersection\n")
        klee_file.write(f"    agent{i}_state_obj_behind_intersection = object_in_range(&info, {i}, 2);\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.obj_behind_intersection, &agent{i}_state_obj_behind_intersection, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_obj_behind_intersection == __soid__agent{i}_state_obj_behind_intersection);\n')

    # tailgating
    for i in range(environment["num_agents"]):
        klee_file.write(f"    // is_tailgating\n")
        klee_file.write(f"    agent{i}_state_is_tailgating = is_tailgating(&info, {i});\n")
        klee_file.write(f'    memmove( &info.agents[{i}].state.is_tailgating, &agent{i}_state_is_tailgating, sizeof(bool)); // Memcopy symb -> struct\n\n')
        klee_file.write(f'    klee_assume( agent{i}_state_is_tailgating == __soid__agent{i}_state_is_tailgating);\n')

    


    klee_file.write(f'    // Klee Close Merge();\n')
    klee_file.write(f'    klee_close_merge();\n')
    
    # handle the q table nd proceed model ONLY FOR AGENT 0
    klee_file.write("    // Q table stuff\n")
    agent = agents['agent0']
    for m in range(1024):
        for n in range(2):
            klee_file.write(f"   info.agents[{0}].q_table[{m}][{n}] = {agent['state']['q_table'][m][n]};\n")


    # Get learning state row
    klee_file.write("\n    // Learning Row\n")
    klee_file.write("    int mrow, __soid__mrow;\n")
    klee_file.write(f'    klee_make_symbolic( &__soid__mrow, sizeof(int), "__soid__mrow_");\n')
    klee_file.write("    mrow = get_learning_state(&info, 0);\n")
    klee_file.write(f'    klee_assume( mrow == __soid__mrow);\n')

    klee_file.write("\n    // Invoke proceed\n")
    
    klee_file.write(f'    bool will_proceed, __soid__will_proceed;\n')
    klee_file.write(f'    klee_make_symbolic( &__soid__will_proceed, sizeof(bool), "__soid__will_proceed");\n')
    klee_file.write("    will_proceed = proceed_model(info.agents[0].q_table, mrow);\n")
    #klee_file.write("    will_proceed = proceed_good_agent(&info, mrow);\n")
    klee_file.write(f'    klee_assume( will_proceed == __soid__will_proceed);\n')
    
    klee_file.write("}\n")
    
    klee_file.close()
    
    #makefile
    makefile = open((klee_prefix + "makefile"),'w', encoding="utf-8")
    
    makefile.write("cc=/tools/soid/soid/llvm-project/release/bin/clang -std=c99\n")
    makefile.write("opt=/tools/soid/soid/llvm-project/release/bin/opt\n")
    makefile.write("link=/tools/soid/soid/llvm-project/release/bin/llvm-link\n")

    # Inbetween files
    makefile.write("BC1=./inter1.bc\n\n")
    makefile.write("BC2=./inter2.bc\n\n")
    makefile.write("BC3=./inter3.bc\n\n")
    makefile.write("BC=./inter.bc\n\n")
    
    # Paths
    makefile.write("KLEE=/tools/soid/soid/klee-float/include/klee\n")
    makefile.write("KEXEC=/tools/soid/soid/klee-float/build/bin/klee\n")
    makefile.write("PRE-LIB-KLEE=-L /tools/soid/soid/klee-float/build/lib/\n")
    makefile.write("POST-LIB-KLEE=-lkleeRuntest\n\n")
    makefile.write("SOIDLIB=/tools/soid/soid/soid/soidlib\n\n")
    makefile.write("symbolic:\n")
    
    # Compile types.c
    makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 /home/mje48/duckietown-soid/src/gym_duckietown/decision_logic/types.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC1)\n")

    # Compile decision_logic.c
    makefile.write("	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 /home/mje48/duckietown-soid/src/gym_duckietown/decision_logic/decision_logic.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC2)\n")

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
    #makefile.write("	rm -rf ./klee-out-*\n")
    #makefile.write("	rm -rf ./klee-last\n")
    
    makefile.close()
    
    
    # print(agents)
    # return file_descriptor, file_path
    return None


if __name__ == '__main__':
    query_blob = json.load(open('src/webserver/soid_files/query_blobs/query_blob'))
    generate_klee_file(query_blob)