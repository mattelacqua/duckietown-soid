#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <stdlib.h>
#include "types.c"

#define STATES 1024
#define ACTIONS 2

/************************************************
 * HELPERS
************************************************/
float pos_distance(double x1, double x2, double z1, double z2){
    double gdistance = (((x2-x1)*(x2-x1)) + ((z2-z1)*(z2-z1)));
    return (float) sqrt(gdistance);
}

bool intersection_dir_agents(EnvironmentInfo* env_info, int agent_index, Direction direction){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    bool dir_waiting_agents = false;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If not us, and at intersection line, and are facing the given direction, and arrive at the SAME TIME
        if (i != agent_index && 
           (agents[i].state.at_intersection_entry || agents[i].state.in_intersection) && 
           agents[i].initial_direction == direction && 
           agents[i].intersection_arrival >= 0 && 
           agents[i].intersection_arrival == agent.intersection_arrival){
            dir_waiting_agents = true;
            break;
        }
    }
    return dir_waiting_agents;
}

bool next_to_go_agents(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    bool next_to_go_agents = false;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If not us, and at intersection line, and are facing the given direction, return true.
        if (i != agent_index && agents[i].state.next_to_go){
            next_to_go_agents = true;
            break;
        }
    }
    return next_to_go_agents;
}

bool intersection_tile(EnvironmentInfo* env_info, int tile_x, int tile_z){
    if (tile_x == env_info->intersection_x && tile_z == env_info->intersection_z)
        return true;
    else
        return false;
}

bool is_behind(EnvironmentInfo* env_info, int agent_index, int other_index){
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    EnvironmentAgent other = env_info->agents.agents_array[other_index];
    // Should always be the same but just in case
    if (agent.direction == other.direction){
        // If north and they are in front of us
        if (agent.direction == NORTH && other.pos_z < agent.pos_z)
            return true;
        // If South and they are in front of us
        else if (agent.direction == SOUTH && other.pos_z > agent.pos_z)
            return true;
        // If EAST and they are in front of us
        else if (agent.direction == EAST && other.pos_x > agent.pos_x)
            return true;
        // If WEST and they are in front of us
        else if (agent.direction == WEST && other.pos_x < agent.pos_x)
            return true;
        else
            return false;

    } else
        return false;
}
/************************************************
 * Intersection Detection
************************************************/

// Check if we are approaching an intersection 
bool intersection_detected(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    if ((agent.direction == NORTH) && 
        (agent.pos_z < agent.stop_z) && 
        agent.state.approaching_intersection)
        return true;
    else if ((agent.direction == WEST) && 
            (agent.pos_x < agent.stop_x) && 
            agent.state.approaching_intersection) 
        return true;
    else if ((agent.direction == SOUTH) && 
            (agent.pos_z > agent.stop_z) && 
            agent.state.approaching_intersection) 
        return true;
    else if ((agent.direction == EAST) && 
            (agent.pos_x > agent.stop_x) && 
            agent.state.approaching_intersection) 
        return true;
    else 
        return false;
}

// Check if we are approaching an intersection 
bool approaching_intersection(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    if ((agent.direction == NORTH) && intersection_tile(env_info, agent.tile_x, agent.tile_z - 1))
        return true;
    else if ((agent.direction == WEST) && intersection_tile(env_info, agent.tile_x - 1, agent.tile_z ))
        return true;
    else if ((agent.direction == SOUTH) && intersection_tile(env_info, agent.tile_x, agent.tile_z + 1 ))
        return true;
    else if ((agent.direction == EAST) && intersection_tile(env_info, agent.tile_x + 1, agent.tile_z ))
        return true;
    else   
        return false;
}



/************************************************
 * STATE FUNCTIONS
************************************************/
bool next_to_go(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    
    // If not at intersection entry, it doesn't matter
    if (!agent.state.at_intersection_entry)
        return false;
    
    // If someone else is next to go then we are not
    if (next_to_go_agents(env_info, agent_index))
        return false;
        
    // General case

    // Is there antoher car in the intersection with ROW
    int ROW_agent_index = -1;
    int lowest_ROW_agent_arrival = 1500;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If not us, at entry, and has right of way
        if (i != agent_index && 
        (agents[i].state.at_intersection_entry || agents[i].state.in_intersection) && 
        agents[i].state.has_right_of_way &&
        agents[i].intersection_arrival < lowest_ROW_agent_arrival){
            ROW_agent_index = i;
            lowest_ROW_agent_arrival = i;
        }
    }

    // If no ROW agent, we have ROW
    if (ROW_agent_index == -1)
        return false;
        
    // Check if we are next in line
    EnvironmentAgent ROW_agent = env_info->agents.agents_array[ROW_agent_index];
    // Check if there is another car that arrive before me
    bool cars_before_me = false;
    bool cars_same_as_me = false;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        if (i != agent_index && 
           (agents[i].state.in_intersection || agents[i].state.at_intersection_entry) && 
           agents[i].intersection_arrival >= 0 && 
           agent.intersection_arrival >= 0 && 
           agents[i].intersection_arrival < agent.intersection_arrival &&
           i != ROW_agent_index){ // Not the same as the one whos turn it is
            cars_before_me = true;
            break;
        }
        if (i != agent_index && 
           (agents[i].state.in_intersection || agents[i].state.at_intersection_entry) && 
           agents[i].intersection_arrival >= 0 && 
           agent.intersection_arrival >= 0 && 
           agents[i].intersection_arrival == agent.intersection_arrival &&
           i != ROW_agent_index){
            cars_same_as_me = true;
        }
    }    
    
    // If theres cars before me after the current ROW one, I'm not next to go
    if (cars_before_me) 
        return false;

    // If theres not cars before me after the current ROW one, and none the same as me, I am next to go
    if (!cars_same_as_me) 
        return true;

    // Figure out which agents have the same arrival time as me and are facing a direction to decide if we go
    bool n_agents = intersection_dir_agents(env_info, agent_index, NORTH);
    bool s_agents = intersection_dir_agents(env_info, agent_index, SOUTH);
    bool e_agents = intersection_dir_agents(env_info, agent_index, EAST);
    bool w_agents = intersection_dir_agents(env_info, agent_index, WEST);

    if (ROW_agent.direction == NORTH) {
        if (agent.direction == EAST)
            return true;
        else if (agent.direction == SOUTH)
            if (!e_agents)
                return true;
            else
                return false;
        else if (agent.direction == WEST)
            if (!e_agents && !s_agents)
                return true;
            else
                return false;
        else if (agent.direction == NORTH)
            return false;
        else  
            return false;
    }
    else if (ROW_agent.direction == EAST) {
        if (agent.direction == SOUTH)
            return true;
        else if (agent.direction == WEST)
            if (!s_agents)
                return true;
            else
                return false;
        else if (agent.direction == NORTH)
            if (!s_agents && !w_agents)
                return true;
            else
                return false;
        else if (agent.direction == EAST)
            return false;
        else  
            return false;
    }
    else if (ROW_agent.direction == SOUTH) {
        if (agent.direction == WEST)
            return true;
        else if (agent.direction == NORTH)
            if (!w_agents)
                return true;
            else
                return false;
        else if (agent.direction == EAST)
            if (!w_agents && !n_agents)
                return true;
            else
                return false;
        else if (agent.direction == SOUTH)
            return false;
        else  
            return false;
    }
    else if (ROW_agent.direction == WEST) {
        if (agent.direction == NORTH)
            return true;
        else if (agent.direction == EAST)
            if (!n_agents)
                return true;
            else
                return false;
        else if (agent.direction == SOUTH)
            if (!n_agents && !e_agents)
                return true;
            else
                return false;
        else if (agent.direction == WEST)
            return false;
        else  
            return false;
    } else 
            return false;
}

// Get right of way for our cars. 
bool has_right_of_way(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    
    // Check if there is another car that arrive before me
    bool cars_before_me = false;
    bool cars_same_as_me = false;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        if (i != agent_index && 
           (agents[i].state.in_intersection || agents[i].state.at_intersection_entry) && 
           agents[i].intersection_arrival >= 0 && 
           agent.intersection_arrival >= 0 && 
           agents[i].intersection_arrival < agent.intersection_arrival){
            cars_before_me = true;
            break;
        }
        if (i != agent_index && 
           (agents[i].state.in_intersection || agents[i].state.at_intersection_entry) && 
           agents[i].intersection_arrival >= 0 && 
           agent.intersection_arrival >= 0 && 
           agents[i].intersection_arrival == agent.intersection_arrival){
            cars_same_as_me = true;
        }
    }    

    // Is there antoher car in the intersection
    bool in_intersection = agent.state.in_intersection;
    bool other_car_in_intersection = !agent.state.intersection_empty;
    bool at_intersection_entry = agent.state.at_intersection_entry;


    // If already in then we must finish
    if(in_intersection)
        return true;

    bool right_of_way = false;
    // If there are cars the same as me, grab our ROW like so
    if (at_intersection_entry){

        // If there is already another car in the intersection we do not have ROW
        if(other_car_in_intersection)
            return false;

        // If cars got there before me, we do not have ROW
        if(cars_before_me)
            return false;

        // If no cars got there the same as me, then its this
        if(!cars_same_as_me)
            return true;        
        
        // Tiebreak for rightmost (intersection_dir_agents checks if matching arrival time)
        Direction direction = agent.direction;
        bool n_agents = intersection_dir_agents(env_info, agent_index, NORTH);
        bool s_agents = intersection_dir_agents(env_info, agent_index, SOUTH);
        bool e_agents = intersection_dir_agents(env_info, agent_index, EAST);
        bool w_agents = intersection_dir_agents(env_info, agent_index, WEST);
        if (direction == NORTH){
            // S
            //E W
            // N
            if (s_agents && e_agents && w_agents)
                right_of_way = true;
            // ?
            //? W
            // N
            else if (w_agents)
                right_of_way = false;
            // ?
            //?  
            // N
            else if (!w_agents)
                right_of_way = true;
            else 
                right_of_way = true;
        }
        else if (direction == EAST){
            // S
            //X W
            // N
            if (n_agents && s_agents && w_agents)
                right_of_way = false;
            // S
            //X W
            // 
            else if (!n_agents && (s_agents && w_agents))
                right_of_way = true;
            // S
            //X 
            // 
            else if (s_agents && !(w_agents || n_agents))
                right_of_way = true;
            // 
            //X W
            // 
            else if (w_agents && !(s_agents || n_agents))
                right_of_way = false;
            // ? 
            //X 
            // N 
            else if (n_agents)
                right_of_way = false;
            else 
                right_of_way = true;
        }
        else if (direction == SOUTH){
            // S
            //E W
            // N
            if (s_agents && e_agents && w_agents)
                right_of_way = false;
            // S
            //E ?
            // ?
            else if (e_agents)
                right_of_way = false;
            // S
            //  W
            // N
            else if (!e_agents && n_agents && w_agents)
                right_of_way = true;
            // S
            //   
            // N
            else if (!e_agents && n_agents && !w_agents)
                right_of_way = false;
            // S
            //   W
            //  
            else if (!e_agents && !n_agents && w_agents)
                right_of_way = true;
            else 
                right_of_way = true;
        }
        else if (direction == WEST){
            // S
            //X W
            // N
            if (n_agents && s_agents && e_agents)
                right_of_way = false;
            // S
            //? W
            // ? 
            else if (s_agents)
                right_of_way = false;
            // 
            //? W
            // ?
            else if (!s_agents)
                right_of_way = true;
            else 
                right_of_way = true;
        } 
        
        return right_of_way;
    } 

    // Not in intersection or at entry
    return true;
}

bool safe_to_enter(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    
    // If we have the right of way its always safe to go.
    if (agent.state.has_right_of_way)
        return true;

    // If we are already in the intersection
    //if (agent.state.in_intersection)
    //    return true;

    // Get the intersection grid positions we will be in
    int intersection_agent_index = -1;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If not us, at entry or in it, and has right of way (could be multiple)
        if (i != agent_index && (
            agents[i].state.at_intersection_entry || agents[i].state.in_intersection)){
            intersection_agent_index = i;

            // Set intersection agent index
            bool intersection_agent_nw = false;
            bool intersection_agent_ne = false;
            bool intersection_agent_sw = false;
            bool intersection_agent_se = false;
            bool agent_nw = false;
            bool agent_ne = false;
            bool agent_sw = false;
            bool agent_se = false;

            EnvironmentAgent intersection_agent = env_info->agents.agents_array[intersection_agent_index];

            // Handle the intersection agent information
            if (intersection_agent.initial_direction == NORTH){
                if (intersection_agent.signal_choice == STRAIGHT){
                    intersection_agent_se = true;
                    intersection_agent_ne = true;
                }
                if (intersection_agent.signal_choice == LEFT){
                    intersection_agent_se = true;
                    intersection_agent_ne = true;
                    intersection_agent_nw = true;
                }
                if (intersection_agent.signal_choice == RIGHT){
                    intersection_agent_se = true;
                }
            }
            if (intersection_agent.initial_direction == EAST){
                if (intersection_agent.signal_choice == STRAIGHT){
                    intersection_agent_sw = true;
                    intersection_agent_se = true;
                }
                if (intersection_agent.signal_choice == LEFT){
                    intersection_agent_sw = true;
                    intersection_agent_se = true;
                    intersection_agent_ne = true;
                }
                if (intersection_agent.signal_choice == RIGHT){
                    intersection_agent_sw = true;
                }
            }   
            if (intersection_agent.initial_direction == SOUTH){
                if (intersection_agent.signal_choice == STRAIGHT){
                    intersection_agent_nw = true;
                    intersection_agent_sw = true;
                }
                if (intersection_agent.signal_choice == LEFT){
                    intersection_agent_nw = true;
                    intersection_agent_sw = true;
                    intersection_agent_se = true;
                }
                if (intersection_agent.signal_choice == RIGHT){
                    intersection_agent_nw = true;
                }
            }
            if (intersection_agent.initial_direction == WEST){
                if (intersection_agent.signal_choice == STRAIGHT){
                    intersection_agent_nw = true;
                    intersection_agent_ne = true;
                }
                if (intersection_agent.signal_choice == LEFT){
                    intersection_agent_ne = true;
                    intersection_agent_nw = true;
                    intersection_agent_sw = true;
                }
                if (intersection_agent.signal_choice == RIGHT){
                    intersection_agent_ne = true;
                }
            } 

            // For our agent
            if (agent.initial_direction == NORTH){
                if (agent.turn_choice == STRAIGHT){
                    agent_se = true;
                    agent_ne = true;
                }
                if (agent.turn_choice == LEFT){
                    agent_se = true;
                    agent_ne = true;
                    agent_nw = true;
                }
                if (agent.turn_choice == RIGHT){
                    agent_se = true;
                }
            }
            if (agent.initial_direction == EAST){
                if (agent.turn_choice == STRAIGHT){
                    agent_sw = true;
                    agent_se = true;
                }
                if (agent.turn_choice == LEFT){
                    agent_sw = true;
                    agent_se = true;
                    agent_ne = true;
                }
                if (agent.turn_choice == RIGHT){
                    agent_sw = true;
                }
            }   
            if (agent.initial_direction == SOUTH){
                if (agent.turn_choice == STRAIGHT){
                    agent_nw = true;
                    agent_sw = true;
                }
                if (agent.turn_choice == LEFT){
                    agent_nw = true;
                    agent_sw = true;
                    agent_se = true;
                }
                if (agent.turn_choice == RIGHT){
                    agent_nw = true;
                }
            }
            if (agent.initial_direction == WEST){
                if (agent.turn_choice == STRAIGHT){
                    agent_nw = true;
                    agent_ne = true;
                }
                if (agent.turn_choice == LEFT){
                    agent_ne = true;
                    agent_nw = true;
                    agent_sw = true;
                }
                if (agent.turn_choice == RIGHT){
                    agent_ne = true;
                }
            } 

            // Check for intersections
            if ((intersection_agent_nw && agent_nw) ||
               (intersection_agent_ne && agent_ne) ||
               (intersection_agent_sw && agent_sw) ||
               (intersection_agent_se && agent_se)){
                return false;
            }
        }
    }
    // No possible collisions return true
    return true;
}
 


// Get the current direction of an agent
char get_direction(float curr_angle){
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
bool in_bounds(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];

    // Check if we are out of the bounds 
    if (agent.pos_x < 0 || agent.pos_z < 0 || agent.pos_x > env_info->grid_w * env_info->road_tile_size || agent.pos_z > env_info->grid_h * env_info->road_tile_size){
        return false;
    } else {
        return true;
    }
}



bool in_intersection(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    if (agent.tile_x == env_info->intersection_x && agent.tile_z == env_info->intersection_z){
        //printf("agent %d in intersection", agent_index);
        return true;
    }
    else
        return false;

}

// Check if we are at the intersection entry
bool at_intersection_entry(EnvironmentInfo* env_info, int agent_index){
    if (in_bounds(env_info, agent_index)){
        EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
        // If we are facing north
        if (agent.direction == NORTH){
            // If we are in the intersection or just below it, check more
            if (in_intersection(env_info, agent_index) || intersection_tile(env_info, agent.tile_x, agent.tile_z - 1)){
                // Check relative to stop line.
                float stop_line = (env_info->intersection_z + 1) * env_info->road_tile_size;
                if (agent.pos_z > stop_line - env_info->robot_length * 0.20 &&
                    agent.pos_z < stop_line + env_info->robot_length)
                    return true;
                else // if not at the stop line
                    return false;
            } else // Not close
                return false;
        }
        else if (agent.direction == WEST){
            // If we are in the intersection or just below it, check more
            if (in_intersection(env_info, agent_index) || intersection_tile(env_info, agent.tile_x-1, agent.tile_z)){
                // Check relative to stop line.
                float stop_line = (env_info->intersection_x + 1) * env_info->road_tile_size;
                if (agent.pos_x > stop_line - env_info->robot_length * 0.20 &&
                    agent.pos_x < stop_line + env_info->robot_length)
                    return true;
                else // if not at the stop line
                    return false;
            } else // Not close
                return false;
        }
        else if (agent.direction == SOUTH){
            // If we are in the intersection or just below it, check more
            if (in_intersection(env_info, agent_index) || intersection_tile(env_info, agent.tile_x, agent.tile_z + 1)){
                // Check relative to stop line.
                int modifier = 0;
                if (env_info->intersection_z == 0)
                    modifier = 1;
                float stop_line = (env_info->intersection_z + modifier) * env_info->road_tile_size;
                if (agent.pos_z > stop_line - env_info->robot_length &&
                    agent.pos_z < stop_line + env_info->robot_length * 0.20)
                    return true;
                else // if not at the stop line
                    return false;
            } else // Not close
                return false;
        }    
        else if (agent.direction == EAST){
            // If we are in the intersection or just below it, check more
            if (in_intersection(env_info, agent_index) || intersection_tile(env_info, agent.tile_x+1, agent.tile_z )){
                // Check relative to stop line.
                int modifier = 0;
                if (env_info->intersection_x == 0)
                    modifier = 1;
                float stop_line = (env_info->intersection_x + modifier) * env_info->road_tile_size;
                if (agent.pos_x > stop_line - env_info->robot_length &&
                    agent.pos_x < stop_line + env_info->robot_length * 0.20)
                    return true;
                else // if not at the stop line
                    return false;
            } else  // if not close
                return false;
        }    
        else  // if no direction
            return false;
    } else  // if our of bounds
        return false;
}

bool cars_arrived_before_me(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If not us, we are both at intersection, and they arrived first
        if (i != agent_index && 
           (agents[i].intersection_arrival >= 0 && agent.intersection_arrival >= 0) && 
           agents[i].intersection_arrival < agent.intersection_arrival){
            // If theyn are at intersection, in it, or approaching it.
            if (agents[i].state.at_intersection_entry || agents[i].state.in_intersection || agents[i].state.approaching_intersection){
                return true;
            }
        }
    }
    return false;
}

bool cars_waiting_to_enter(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If not us, and are at the intersection entry
        if (i != agent_index && agents[i].state.at_intersection_entry)
            return true;
    }
    return false;
}

bool intersection_empty(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If someone is in the intersection
        if (i != agent_index && agents[i].state.in_intersection)
            return false;
    }
    return true;
}

bool object_in_range(EnvironmentInfo* env_info, int agent_index, int location){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    float radius = agent.lookahead;
    if (!in_bounds(env_info, agent_index))
        return false;
    else {
        Direction direction = agent.direction;
        float side_radius = radius / 10.0;
        float front_radius = radius;
        float robot_length = env_info->robot_length;
        
        // Initialiaze bounds
        float object_ahead_range_z_lb = 0.0;
        float object_ahead_range_z_ub = 0.0;
        float object_ahead_range_x_lb = 0.0;
        float object_ahead_range_x_ub = 0.0;
        // location 1 = ahead 2 = behind
        if (direction == NORTH){
            if (location == 1){ // ahead
                object_ahead_range_z_lb = agent.pos_z;
                object_ahead_range_z_ub = agent.pos_z + front_radius;
            } 
            else if (location == 2){ // behind
                object_ahead_range_z_lb = agent.pos_z - front_radius - robot_length;
                object_ahead_range_z_ub = agent.pos_z - robot_length;
            }
            object_ahead_range_x_lb = agent.pos_x - side_radius;
            object_ahead_range_x_ub = agent.pos_x + side_radius;
        }
        else if (direction == SOUTH){
            if (location == 1){ // ahead
                object_ahead_range_z_lb = agent.pos_z - front_radius;
                object_ahead_range_z_ub = agent.pos_z;
            } 
            else if (location == 2){ // behind
                object_ahead_range_z_lb = agent.pos_z + robot_length;
                object_ahead_range_z_ub = agent.pos_z + front_radius + robot_length;
            }
            object_ahead_range_x_lb = agent.pos_x - side_radius;
            object_ahead_range_x_ub = agent.pos_x + side_radius;
        }
        else if (direction == WEST){
            if (location == 1){ // ahead
                object_ahead_range_x_lb = agent.pos_x - front_radius;
                object_ahead_range_x_ub = agent.pos_x;
            } 
            else if (location == 2){ // behind
                object_ahead_range_x_lb = agent.pos_x + robot_length;
                object_ahead_range_x_ub = agent.pos_x + front_radius + robot_length;
            }
            object_ahead_range_z_lb = agent.pos_z - side_radius;
            object_ahead_range_z_ub = agent.pos_z + side_radius;
        }
        else if (direction == EAST){
            if (location == 1){ // ahead
                object_ahead_range_x_lb = agent.pos_x;
                object_ahead_range_x_ub = agent.pos_x + front_radius;
            } 
            else if (location == 2){ // behind
                object_ahead_range_x_lb = agent.pos_x - front_radius - robot_length;
                object_ahead_range_x_ub = agent.pos_x - robot_length;
            }
            object_ahead_range_z_lb = agent.pos_z - side_radius;
            object_ahead_range_z_ub = agent.pos_z + side_radius;
        }

        // Once bounds are initilized, check if any agent falls inside of them.
        for (int i = 0; i < env_info->agents.num_agents; i++){
            // if not us and in the bounds
            if (i != agent_index && 
               (agents[i].pos_x >= object_ahead_range_x_lb) &&
               (agents[i].pos_x <= object_ahead_range_x_ub) &&
               (agents[i].pos_z >= object_ahead_range_x_lb) &&
               (agents[i].pos_z <= object_ahead_range_x_ub))
                return true;
        }
        
        // If none are in the bounds there is no object in range.
        return false;
    }
}

// Check if a car is entering our range
bool car_entering_range(EnvironmentInfo* env_info, int agent_index, int location){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    float radius = agent.lookahead;
    float radius_multiplier = 1.5;
    if (!in_bounds(env_info, agent_index))
        return false;
    else {
        Direction direction = agent.direction;
        float side_radius = radius / 10.0;
        float front_radius = radius;
        float robot_length = env_info->robot_length;
        
        // Initialiaze bounds
        float object_ahead_range_z_lb = 0.0;
        float object_ahead_range_z_ub = 0.0;
        float object_ahead_range_x_lb = 0.0;
        float object_ahead_range_x_ub = 0.0;
        // location 1 = ahead 2 = behind
        if (direction == NORTH){
            if (location == 1){ // ahead
                object_ahead_range_z_lb = agent.pos_z + front_radius;
                object_ahead_range_z_ub = agent.pos_z + front_radius * radius_multiplier;
            } 
            else if (location == 2){ // behind
                object_ahead_range_z_lb = agent.pos_z - (front_radius * radius_multiplier) - robot_length;
                object_ahead_range_z_ub = agent.pos_z - front_radius - robot_length;
            }
            object_ahead_range_x_lb = agent.pos_x - side_radius;
            object_ahead_range_x_ub = agent.pos_x + side_radius;
        }
        else if (direction == SOUTH){
            if (location == 1){ // ahead
                object_ahead_range_z_lb = agent.pos_z - (front_radius * radius_multiplier);
                object_ahead_range_z_ub = agent.pos_z - front_radius ;
            } 
            else if (location == 2){ // behind
                object_ahead_range_z_lb = agent.pos_z + front_radius + robot_length;
                object_ahead_range_z_ub = agent.pos_z + (front_radius * radius_multiplier) + robot_length;
            }
            object_ahead_range_x_lb = agent.pos_x - side_radius;
            object_ahead_range_x_ub = agent.pos_x + side_radius;
        }
        else if (direction == WEST){
            if (location == 1){ // ahead
                object_ahead_range_x_lb = agent.pos_x - (front_radius * radius_multiplier);
                object_ahead_range_x_ub = agent.pos_x - front_radius;
            } 
            else if (location == 2){ // behind
                object_ahead_range_x_lb = agent.pos_x + front_radius + robot_length;
                object_ahead_range_x_ub = agent.pos_x + (front_radius * radius_multiplier) + robot_length;
            }
            object_ahead_range_z_lb = agent.pos_z - side_radius;
            object_ahead_range_z_ub = agent.pos_z + side_radius;
        }
        else if (direction == EAST){
            if (location == 1){ // ahead
                object_ahead_range_x_lb = agent.pos_x + front_radius;
                object_ahead_range_x_ub = agent.pos_x + (front_radius * radius_multiplier);
            } 
            else if (location == 2){ // behind
                object_ahead_range_x_lb = agent.pos_x - (front_radius * radius_multiplier) - robot_length;
                object_ahead_range_x_ub = agent.pos_x - front_radius - robot_length;
            }
            object_ahead_range_z_lb = agent.pos_z - (front_radius * radius_multiplier);
            object_ahead_range_z_ub = agent.pos_z + side_radius;
        }

        // Once bounds are initilized, check if any agent falls inside of them.
        for (int i = 0; i < env_info->agents.num_agents; i++){
            // if not us and in the bounds and is getting closer to us
            if (i != agent_index && 
               (agents[i].pos_x >= object_ahead_range_x_lb) &&
               (agents[i].pos_x <= object_ahead_range_x_ub) &&
               (agents[i].pos_z >= object_ahead_range_x_lb) &&
               (agents[i].pos_z <= object_ahead_range_x_ub) &&
               (pos_distance((double) agents[i].pos_x, (double) agent.pos_x, (double) agents[i].pos_z, (double)agent.pos_z) < pos_distance((double) agents[i].prev_pos_x, (double) agent.prev_pos_x, (double)agents[i].prev_pos_z, (double) agent.prev_pos_z)))
                return true;
        }
        
        // If none are in the bounds there is no object in range.
        return false;
    }
}

bool is_tailgating(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent *agents = env_info->agents.agents_array;
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    for (int i = 0; i < env_info->agents.num_agents; i++){
        // If not us, going the same direction, and we are behind them
        if (i != agent_index && 
           agents[i].direction == agent.direction && 
           is_behind(env_info, agent_index, i)){
            float curr_distance = (float) pos_distance((double)agent.pos_x, (double)agents[i].pos_x, (double)agent.pos_z, (double)agents[i].pos_z);
            //printf("curr_distance behind %f\n", curr_distance);
            if (curr_distance < (env_info->robot_length * 2.5))
                return true;
        }
    }
    return false;
}



// Good agent proceed: 0=stop 1=proceed

bool proceed_good_agent(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    if (agent.state.is_tailgating || !agent.state.safe_to_enter) 
        return false;
    if (agent.state.has_right_of_way || agent.state.safe_to_enter) 
        return true;
    else {
        if (agent.patience > 100) 
            return true;
        else 
            return false;
    }

}

// Handle patience return 0=do nothing 1=inc 2=reset
int handle_patience(EnvironmentInfo* env_info, int agent_index){
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    if (!(agent.state.has_right_of_way || agent.state.safe_to_enter) && agent.state.next_to_go && agent.state.intersection_empty)
        return 1;
    if (!(agent.state.has_right_of_way || agent.state.safe_to_enter) && agent.state.next_to_go && !agent.state.intersection_empty)
        return 2;
    return 0;
}

// Read the model to see if we proceed
bool proceed_model(float model[STATES][ACTIONS], int state) {
    float stay = model[state][0];
    float move = model[state][1];
    if (move >= stay) return true;
    else return false; 

}


// Get the learning state we are in.
int get_learning_state(EnvironmentInfo* env_info, int agent_index){
    /*************************************************************
    # 0: in an intersection +512
    # 1: at intersection entry +256
    # 2: intersection is empty +128
    # 3: approaching an intersection +64
    # 4: object in range +32
    # 5: we have the right of way +16
    # 6: cars waiting to get in +8
    # 7: car entering our range +4
    # 8: safe to enter 
    # 9: tailgating +1 
    *************************************************************/
    EnvironmentAgent agent = env_info->agents.agents_array[agent_index];
    int model_row = 0;
    
    if (agent.state.in_intersection)
        model_row += 512;
    if (agent.state.at_intersection_entry)
        model_row += 256;
    if (agent.state.intersection_empty)
        model_row += 128;
    if (agent.state.approaching_intersection)
        model_row += 64;
    if (agent.state.obj_in_range)
        model_row += 32;
    if (agent.state.has_right_of_way)
        model_row += 16;
    if (agent.state.cars_waiting_to_enter)
        model_row += 8;
    if (agent.state.car_entering_range)
        model_row += 4;
    if (agent.state.safe_to_enter)
        model_row += 2;
    if (agent.state.is_tailgating)
        model_row += 1;
    
    return model_row;

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
    int num_agents = env_info->agents.num_agents;
    fflush(stdout);
    printf("Environment information: \n");
    printf("Intersection: %d, %d\n", intersection_x, intersection_z);
    printf("Grid Height: %d Grid Width %d Road tile size: %f\n", grid_h, grid_w, road_tile_size);
    printf("Robot Length: %f Max Steps: %d\n",  robot_length, max_steps);
    
    EnvironmentAgent *agents = env_info->agents.agents_array;
    for (int i = 0; i < num_agents; i++) {
        printf("Agent %d information \n", agents[i].id);
        printf("pos_x: %f pos_z %f \n", agents[i].pos_x, agents[i].pos_z);
        printf("prev_pos_x: %f prev_pos_z %f \n", agents[i].prev_pos_x, agents[i].prev_pos_z);
        printf("stop_x: %f stop_z %f \n", agents[i].stop_x, agents[i].stop_z);
        printf("tile_x: %d tile_z %d \n", agents[i].tile_x, agents[i].tile_z);
        printf("turn_choice: %d signal_choice %d \n", agents[i].turn_choice, agents[i].signal_choice);
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
        printf("%d safe_to_enter\n", agents[i].state.safe_to_enter);
        printf("%d is_tailgating\n\n", agents[i].state.is_tailgating);
    }
}

