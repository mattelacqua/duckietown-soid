#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <stdlib.h>
#include "types.c"

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
            wait_step += intersection_arrival - env_agent_array_struct->ENV_AGENT_ARRAY[i].intersection_arrival;
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
