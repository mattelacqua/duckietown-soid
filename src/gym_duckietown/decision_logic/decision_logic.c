#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <stdlib.h>
#include "types.c"

#define STATES 1024
#define ACTIONS 2

// Check if we are approaching an intersection 
bool intersection_detected(Direction direction, float curr_x, float curr_z, float stop_x, float stop_z, bool approaching_intersection) 
{
    if ((direction == NORTH) && (curr_z < stop_z) && approaching_intersection) {
        return true;
    } 
    else  if ((direction == WEST) && (curr_x < stop_x) && approaching_intersection){
        return true;
    }
    else  if ((direction == SOUTH) && (curr_z > stop_z) && approaching_intersection){
        return true;
    }
    else  if ((direction == EAST) && (curr_x > stop_x) && approaching_intersection){
        return true;
    } else {
        return false;
    }
}

// Get the current direction of an agent
char get_direction(int curr_angle){
    if (curr_angle > 45 && curr_angle <= 135) {
        return 'N';
    }
    else if (curr_angle > 135 && curr_angle <= 225){
        return 'W';
    }
    else if (curr_angle > 225 && curr_angle <= 315){
        return 'S';
    }
    else{
        return 'E';
    }
}

// Get if we are in bounds or not
bool in_bounds(float curr_pos_x, float curr_pos_y, int grid_width, int grid_height, float road_tile_size){
    // Check if we are out of the bounds 
    if (curr_pos_x < 0 || curr_pos_y < 0 || curr_pos_x > grid_width * road_tile_size || curr_pos_y > grid_height * road_tile_size){
        return false;
    } else {
        return true;
    }
}

// Get the turn choice TODO move to utils
TurnChoice get_turn(TurnChoice choice) {
    if (choice == RANDOM) {
        srand(time(NULL));   // Initialization, should only be called once.
        int r = rand() % 3;
        return r;
    }
    else {
        return choice;
    }
}

// Get the signal choice TODO MOve to utils
TurnChoice get_signal(TurnChoice turn_choice, TurnChoice signal_choice) {
    if (signal_choice == RANDOM) {
        return turn_choice;
    }
    else {
        return signal_choice;
    }
}

IntersectionAction *intersection_action(TurnChoice old_turn_choice, TurnChoice old_signal_choice, int intersection_arrival, EnvironmentAgentArray* env_agent_array_struct) {
    
    // Incase of random turn or signal
    TurnChoice turn_choice = get_turn(old_turn_choice);
    TurnChoice signal_choice = get_signal(turn_choice, old_signal_choice);
    Action action = STOP;

    // Check if we want to wait first
    int num_near_intersection = env_agent_array_struct->elements;

    int wait_step = 0;

    for (int i = 0; i < num_near_intersection; i++) {
        if (intersection_arrival > env_agent_array_struct->ENV_AGENT_ARRAY[i].intersection_arrival) {
            //wait_step += intersection_arrival - env_agent_array_struct->ENV_AGENT_ARRAY[i].intersection_arrival;
            wait_step +=25 ;
        }
    }
    
    // Check if we have the right of way (No other cars are in intersection)
    // Convert to right action
    action = INTERSECTION_FORWARD;
    
    // Return our action
    IntersectionAction *intersection_action;
    intersection_action = make_action(turn_choice, signal_choice, action);

    return intersection_action;
}

// Get right of way for our cars. 
bool has_right_of_way(  bool in_intersection, 
                    bool other_car_in_intersection, 
                    bool at_intersection_entry, 
                    Direction direction, 
                    bool n_agents, 
                    bool s_agents, 
                    bool e_agents, 
                    bool w_agents){
    // If already in then we must finish
    bool already_in = false;
    //if(in_intersection && !at_intersection_entry){
    if(in_intersection){
        already_in = true;
    }
    bool other_car_in = false;
    if(other_car_in_intersection && at_intersection_entry) {
        other_car_in = true;
    }

    bool right_of_way = false;
    if (at_intersection_entry){

        if (direction == NORTH){
            // S
            //E W
            // N
            if (s_agents && e_agents && w_agents){
                right_of_way = true;
            }
            // ?
            //? W
            // N
            else if (w_agents){
                right_of_way = false;
            }
            // ?
            //?  
            // N
            else if (!w_agents){
                right_of_way = true;
            }
            else {
                right_of_way = true;
            }
        }
        else if (direction == EAST){
            // S
            //X W
            // N
            if (n_agents && s_agents && w_agents){
                right_of_way = false;
            }
            // S
            //X W
            // 
            else if (!n_agents && (s_agents && w_agents)){
                right_of_way = true;
            }
            // S
            //X 
            // 
            else if (s_agents && !(w_agents || n_agents)){
                right_of_way = true;
            }
            // 
            //X W
            // 
            else if (w_agents && !(s_agents || n_agents)){
                right_of_way = false;
            }
            // ? 
            //X 
            // N 
            else if (n_agents){
                right_of_way = false;
            }
            else {
                right_of_way = true;
            }
        }
        else if (direction == SOUTH){
            // S
            //E W
            // N
            if (s_agents && e_agents && w_agents){
                right_of_way = false;
            }
            // S
            //E ?
            // ?
            else if (e_agents){
                right_of_way = false;
            }
            // S
            //  W
            // N
            else if (!e_agents && n_agents && w_agents){
                right_of_way = true;
            }
            // S
            //   
            // N
            else if (!e_agents && n_agents && !w_agents){
                right_of_way = false;
            }
            // S
            //   W
            //  
            else if (!e_agents && !n_agents && w_agents){
                right_of_way = true;
            }
            else {
                right_of_way = true;
            }
        }
        else if (direction == WEST){
            // S
            //X W
            // N
            if (n_agents && s_agents && e_agents){
                right_of_way = false;
            }
            // S
            //? W
            // ? 
            else if (s_agents){
                right_of_way = false;
            }
            // 
            //? W
            // ?
            else if (!s_agents){
                right_of_way = true;
            }
            else {
                right_of_way = true;
            }
        } 
        // If already in intersection, we have row
        if(already_in){
            return true;
        } 
        
        // If other car is in and we don't have ROW, then don't go
        else if (other_car_in) {
            return false;
        } 
        
        // If another car is in but we have the real rigght of way, lets go anyways 25% of the time.
        /*else if (other_car_in && right_of_way){

            if (rand() % 100 < 25){
                return false;
            }
            else{
                return false;
            }
        }*/

        // any strange case
        else{
            return right_of_way;
        }    
    } 
    else {
        return true;
    }
}
    


// Good agent proceed: 0=stop 1=proceed
bool proceed_good_agent(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.ENV_AGENT_ARRAY[agent_index];
    if (agent.state.is_tailgating) 
        return false;
    if (agent.state.has_right_of_way) 
        return true;
    if (!agent.state.has_right_of_way){
        if (agent.patience > 100) 
            return true;
        else 
            return false;
    }
}

// Handle patience return 0=do nothing 1=inc 2=reset
int handle_patience(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.ENV_AGENT_ARRAY[agent_index];
    if (!agent.state.has_right_of_way && agent.state.next_to_go && agent.state.intersection_empty)
        return 1;
    if (!agent.state.has_right_of_way && agent.state.next_to_go && !agent.state.intersection_empty)
        return 2;
    return 0;
}

// Read the model to see if we proceed
bool proceed_model(float model[STATES][ACTIONS], int state) {
    float stay = model[state][0];
    float move = model[state][1];
    if (move >= stay) return true;
    if (stay > move) return false; 
}


// Read the model to see if we proceed
void print_all(EnvironmentInfo* env_info) {
    int intersection_x = env_info->intersection_x;
    int intersection_z = env_info->intersection_z;
    float robot_length = env_info->robot_length;
    int grid_w = env_info->grid_w;
    int grid_h = env_info->grid_h;
    float road_tile_size = env_info->road_tile_size;
    int max_steps = env_info->max_steps;
    int num_agents = env_info->agents.elements;
    fflush(stdout);
    printf("Environment information: \n");
    printf("Intersection: %d, %d\n", intersection_x, intersection_z);
    printf("Grid Height: %d Grid Width %d Road tile size: %f\n", grid_h, grid_w, road_tile_size);
    printf("Robot Length: %f Max Steps: %d\n",  robot_length, max_steps);
    
    EnvironmentAgent *agents = env_info->agents.ENV_AGENT_ARRAY;
    for (int i = 0; i < num_agents; i++) {
        printf("Agent %d information \n", agents[i].id);
        printf("pos_x: %f pos_z %f \n", agents[i].pos_x, agents[i].pos_z);
        printf("prev_pos_x: %f prev_pos_z %f \n", agents[i].prev_pos_x, agents[i].prev_pos_z);
        printf("stop_x: %f stop_z %f \n", agents[i].stop_x, agents[i].stop_z);
        printf("tile_x: %d tile_z %d \n", agents[i].tile_x, agents[i].tile_z);
        printf("angle: %f speed: %f forward_step: %f direction: %d intersection_arrival: %d step_count: %d\n", 
            agents[i].angle, 
            agents[i].speed, 
            agents[i].forward_step, 
            agents[i].direction, 
            agents[i].intersection_arrival, 
            agents[i].step_count);
        printf("%d in_intersection \n", agents[i].state.in_intersection);
        printf("%d at_intersection_entry\n", agents[i].state.at_intersection_entry);
        printf("%d intersection_empty\n", agents[i].state.intersection_empty);
        printf("%d approaching_intersection\n", agents[i].state.approaching_intersection);
        printf("%d obj_in_range\n", agents[i].state.obj_in_range);
        printf("%d has_right_of_way\n", agents[i].state.has_right_of_way);
        printf("%d cars_waiting_to_enter\n", agents[i].state.cars_waiting_to_enter);
        printf("%d car_entering_range\n", agents[i].state.car_entering_range);
        printf("%d obj_behind_intersection\n", agents[i].state.obj_behind_intersection);
        printf("%d is_tailgating\n\n", agents[i].state.is_tailgating);
    }


}