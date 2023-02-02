#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <stdlib.h>
#include "types.h"

#ifndef DL_H
#define DL_H

#define STATES 1024
#define ACTIONS 2

/************************************************
 * HELPERS
************************************************/
// Return a size 2 array of tile positions, index 0 is x, index 1 is z
TilePos get_tile_pos(float pos_x, float pos_z, float road_tile_size);

StopPos get_stop_pos(int tile_x, int tile_z, float road_tile_size, Direction direction, float speed);

float pos_distance(double x1, double x2, double z1, double z2);

bool intersection_dir_agents(EnvironmentInfo* env_info, int agent_index, Direction direction);

bool next_to_go_agents(EnvironmentInfo* env_info, int agent_index);

bool intersection_tile(EnvironmentInfo* env_info, int tile_x, int tile_z);

bool is_behind(EnvironmentInfo* env_info, int agent_index, int other_index);

// Check if we are approaching an intersection 
bool intersection_detected(EnvironmentInfo* env_info, int agent_index);

// Check if we are approaching an intersection 
bool approaching_intersection(EnvironmentInfo* env_info, int agent_index);

bool next_to_go(EnvironmentInfo* env_info, int agent_index);

// Get right of way for our cars. 
bool has_right_of_way(EnvironmentInfo* env_info, int agent_index);

bool safe_to_enter(EnvironmentInfo* env_info, int agent_index);
 


// Get the current direction of an agent
char get_direction(float curr_angle);

Direction get_dl_direction(float curr_angle);

// Get if we are in bounds or not
bool in_bounds(EnvironmentInfo* env_info, int agent_index);



bool in_intersection(EnvironmentInfo* env_info, int agent_index);

// Check if we are at the intersection entry
bool at_intersection_entry(EnvironmentInfo* env_info, int agent_index);

bool cars_arrived_before_me(EnvironmentInfo* env_info, int agent_index);

bool cars_waiting_to_enter(EnvironmentInfo* env_info, int agent_index);

bool intersection_empty(EnvironmentInfo* env_info, int agent_index);

bool object_in_range(EnvironmentInfo* env_info, int agent_index, int location);

// Check if a car is entering our range
bool car_entering_range(EnvironmentInfo* env_info, int agent_index, int location);

bool is_tailgating(EnvironmentInfo* env_info, int agent_index);


// Good agent proceed: 0=stop 1=proceed
bool proceed_good_agent(EnvironmentInfo* env_info, int agent_index);

// Handle patience return 0=do nothing 1=inc 2=reset
int handle_patience(EnvironmentInfo* env_info, int agent_index);

// Read the model to see if we proceed
bool proceed_model(float model[STATES][ACTIONS], int state) ;


// Get the learning state we are in.
int get_learning_state(EnvironmentInfo* env_info, int agent_index);

// Read the model to see if we proceed
void print_all(EnvironmentInfo* env_info) ;


#endif