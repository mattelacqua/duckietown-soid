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

bool proceed(AgentState agent_state, bool good_agent) {
    /*fflush(stdout);
    printf("In Intersection: %d \n", agent_state.in_intersection);
    printf("At Entry: %d \n", agent_state.at_entry);
    printf("Intersection Empty:%d \n", agent_state.intersection_empty);
    printf("Intersection In Range: %d \n", agent_state.intersection_in_range);
    printf("Object In Range: %d \n", agent_state.object_in_range);
    printf("Ahead Car Intersection In Range: %d \n", agent_state.ahead_car_intersection_in_range);
    printf("Ahead Car Object In Range: %d \n", agent_state.ahead_car_object_in_range);
    printf("Car Entering Our Range: %d \n", agent_state.car_entering_our_range);
    printf("Car Behind Us In Intersectione: %d \n", agent_state.car_behind_us_in_intersection);
    printf("Car Behind Us Out Intersectione: %d \n", agent_state.car_behind_us_out_intersection);
    

    fflush(stdout);*/
    // If we are the learning agent then learning code will go here. Else, just behave w/ common sense
    //if (!good_agent){
        if (agent_state.object_in_range)
            return false;
        else
            return true;
    /*} else {
        // If we are going to hit a car in intersection or outside of
        if (agent_state.object_in_rangery)
            return false;
        // If there are cars in range, we are at intersection,  stop
        else if (agent_state.object_in_range && agent_state.at_entry)
            return false;
        // If we are at intersection, and its not empty stop
        else if (agent_state.at_entry && !agent_state.intersection_empty)
            return false;
        // If we are at intersection, and its empty, go
        else if (agent_state.at_entry && agent_state.intersection_empty)
            return true;
        else
            return true;
    }*/
}


