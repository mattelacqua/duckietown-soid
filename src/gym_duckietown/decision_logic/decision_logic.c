#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <stdlib.h>
#include "types.c"

#define STATES 1024
#define ACTIONS 2

// Check if we are in the middle of completing an action
bool completing_action(Action action) {
    if(action == NO_ACTION) {
        return false;
    } else {
        return true;
    }
}

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
    if (turn_choice == STRAIGHT){
        action = INTERSECTION_FORWARD;
    }
    else if (turn_choice == LEFT){
        action = INTERSECTION_LEFT;
    }
    else if (turn_choice == RIGHT){
        action = INTERSECTION_RIGHT;
    }
    
    // Return our action
    IntersectionAction *intersection_action;
    intersection_action = make_action(turn_choice, signal_choice, action, wait_step);

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
    if(in_intersection && !at_intersection_entry){
        return true;
    }
    if(other_car_in_intersection && at_intersection_entry) {
        return false;
    }

    if (at_intersection_entry){
        if (direction == NORTH){
            // S
            //E W
            // N
            if (s_agents && e_agents && w_agents){
                return true;
            }
            // ?
            //? W
            // N
            else if (w_agents){
                return false;
            }
            // ?
            //?  
            // N
            else if (!w_agents){
                return true;
            }
            else {
                return true;
            }
        }
        else if (direction == EAST){
            // S
            //X W
            // N
            if (n_agents && s_agents && w_agents){
                return false;
            }
            // S
            //X W
            // 
            else if (!n_agents && (s_agents && w_agents)){
                return true;
            }
            // S
            //X 
            // 
            else if (s_agents && !(w_agents || n_agents)){
                return true;
            }
            // 
            //X W
            // 
            else if (w_agents && !(s_agents || n_agents)){
                return false;
            }
            // ? 
            //X 
            // N 
            else if (n_agents){
                return false;
            }
            else {
                return true;
            }
        }
        else if (direction == SOUTH){
            // S
            //E W
            // N
            if (s_agents && e_agents && w_agents){
                return false;
            }
            // S
            //E ?
            // ?
            else if (e_agents){
                return false;
            }
            // S
            //  W
            // N
            else if (!e_agents && n_agents && w_agents){
                return true;
            }
            // S
            //   
            // N
            else if (!e_agents && n_agents && !w_agents){
                return false;
            }
            // S
            //   W
            //  
            else if (!e_agents && !n_agents && w_agents){
                return true;
            }
            else {
                return true;
            }
        }
        else if (direction == WEST){
            // S
            //X W
            // N
            if (n_agents && s_agents && e_agents){
                return false;
            }
            // S
            //? W
            // ? 
            else if (s_agents){
                return false;
            }
            // 
            //? W
            // ?
            else if (!s_agents){
                return true;
            }
            else {
                return true;
            }
        } 
    } 
    else{
        return true;
    }
}
    



// Read the model to see if we proceed
bool proceed(float model[STATES][ACTIONS], int state) {
    float stay = model[state][0];
    float move = model[state][1];
    if (move >= stay) return true;
    if (stay > move) return false; 
}


