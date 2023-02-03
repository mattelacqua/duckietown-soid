#include <string.h>
#include "../../../gym_duckietown/decision_logic/decision_logic.h"

#include "/tools/soid/soid/soid/soidlib/soidlib.h"
int main(int argc, char **argv) {
    EnvironmentInfo info;
    klee_open_merge();

    // Environment Information:
    info.intersection_x = 2;
    info.intersection_z = 2;
    info.robot_length = 0.18;
    info.grid_w = 5;
    info.grid_h = 5;
    info.road_tile_size = 0.585;
    info.max_steps = 1500;
    info.num_agents = 2;

    // Agent Array:

    // Agent0 Information:
    info.agents[0].id = 0;
    float agent0_pos_x, agent0_pos_z, agent0_angle, agent0_forward_step, agent0_speed, agent0_lookahead;
    int agent0_signal_choice, agent0_turn_choice, agent0_initial_direction, agent0_intersection_arrival, agent0_step_count, agent0_patience;
    klee_make_symbolic( &agent0_pos_x, sizeof(float), "agent0_pos_x");
    klee_make_symbolic( &agent0_pos_z, sizeof(float), "agent0_pos_z");
    klee_make_symbolic( &agent0_angle, sizeof(float), "agent0_angle");
    klee_make_symbolic( &agent0_forward_step, sizeof(float), "agent0_forward_step");
    klee_make_symbolic( &agent0_speed, sizeof(float), "agent0_speed");
    klee_make_symbolic( &agent0_lookahead, sizeof(float), "agent0_lookahead");
    klee_make_symbolic( &agent0_signal_choice, sizeof(TurnChoice), "agent0_signal_choice");
    klee_make_symbolic( &agent0_turn_choice, sizeof(TurnChoice), "agent0_turn_choice");
    klee_make_symbolic( &agent0_initial_direction, sizeof(Direction), "agent0_initial_direction");
    klee_make_symbolic( &agent0_intersection_arrival, sizeof(int), "agent0_intersection_arrival");
    klee_make_symbolic( &agent0_patience, sizeof(int), "agent0_patience");
    klee_make_symbolic( &agent0_step_count, sizeof(int), "agent0_step_count");
    klee_assume( agent0_pos_x == (float) 1.585 ); // Concrete Val 
    klee_assume( agent0_pos_z == (float) 1.842 ); // Concrete Val 
    klee_assume( agent0_angle == (float) 1.588 ); // Concrete Val 
    klee_assume( agent0_forward_step == (float) 0.44 ); // Concrete Val 
    klee_assume( agent0_speed == (float) 0.003 ); // Concrete Val 
    klee_assume( agent0_signal_choice == RIGHT ); // Concrete Val 
    klee_assume( agent0_turn_choice == RIGHT ); // Concrete Val 
    klee_assume( agent0_lookahead == (float) 0.585); // Concrete State Val 
    klee_assume( agent0_intersection_arrival == 77); // Concrete State Val 
    klee_assume( agent0_initial_direction == 0); // Concrete State Val 
    klee_assume( agent0_patience == 0); // Concrete State Val 
    klee_assume( agent0_step_count == 107); // Concrete State Val 
