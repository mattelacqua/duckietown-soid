#include "src/gym_duckietown/decision_logic/types.c"
#include "src/gym_duckietown/decision_logic/decision_logic.c"

int main(int argc, char **argv) {
    EnvironmentInfo *info = malloc(sizeof(EnvironmentInfo));
    klee_open_merge();

    // Environment Information:
    info->intersection_x = 2;
    info->intersection_z = 2;
    info->robot_length = 0.18;
    info->grid_w = 5;
    info->grid_h = 5;
    info->road_tile_size = 0.585;
    info->max_steps = 1500;

    // Agent Array:
    EnvironmentAgentArray *agents = malloc(sizeof(EnvironmentAgentArray));
    agents->num_agents = 3;    info->agents = *agents;
    // Agent0 Information:
    EnvironmentAgent agent0 = agents->agents_array[0];
    agent0.id = 0;
    klee_make_symbolic( &agent0.pos_x, sizeof(float), "pos_x");
    klee_make_symbolic( &agent0.pos_z, sizeof(float), "pos_z");
    klee_make_symbolic( &agent0.angle, sizeof(float), "angle");
    klee_make_symbolic( &agent0.forward_step, sizeof(float), "forward_step");
    klee_make_symbolic( &agent0.lookahead, sizeof(float), "lookahead");
    klee_make_symbolic( &agent0.signal_choice, sizeof(TurnChoice), "signal_choice");
    klee_make_symbolic( &agent0.turn_choice, sizeof(TurnChoice), "turn_choice");
    klee_make_symbolic( &agent0.initial_direction, sizeof(Direction), "initial_direction");
    klee_make_symbolic( &agent0.intersection_arrival, sizeof(int), "intersection_arrival");
    klee_make_symbolic( &agent0.patience, sizeof(int), "patience");
    klee_make_symbolic( &agent0.step_count, sizeof(int), "step_count");
    klee_assume( agent0.pos_x == 1.316 ); // Concrete Val 
    klee_assume( agent0.pos_z == 0.136 ); // Concrete Val 
    klee_assume( agent0.angle == 4.712 ); // Concrete Val 
    klee_assume( agent0.forward_step == 0.51 ); // Concrete Val 
    klee_assume( agent0.signal_choice == "Right" ); // Concrete Val 
    klee_assume( agent0.turn_choice == "Right" ); // Concrete Val 
    klee_assume( agent0.initial_direction == 1 ); // Concrete Val 
    klee_assume( agent0.intersection_arrival == -1); // Concrete Val 
    klee_assume( agent0.lookahead == 0.585); // Concrete Val 
    agent0.prev_pos_z = agent0.pos_x; // Calculated Variable
    agent0.prev_pos_z = agent0.pos_z; // Calculated Variable
    agent0.direction = get_direction(agent0.angle/3.14*180); // Calculated Variable
    TilePos *agent0_tile_pos = get_tile_pos(agent0.pos_x, agent0.pos_z, info->road_tile_size); // Calculated Variable
    agent0.tile_x = agent0_tile_pos->x; // Calculated Variable
    agent0.tile_z = agent0_tile_pos->z; // Calculated Variable
    StopPos *agent0_stop_pos = get_stop_pos(agent0.tile_x, agent0.tile_z, info->road_tile_size, agent0.direction, agent0.speed); // Calculated Variable
    agent0.stop_x = agent0_stop_pos->x; // Calculated Variable
    agent0.stop_z = agent0_stop_pos->z; // Calculated Variable
    agent0.exists = true; // exist 

    agent0.state.in_intersection = false; //initial states
    agent0.state.at_intersection_entry = false; //initial states
    agent0.state.intersection_empty = false; //initial states
    agent0.state.approaching_intersection = false; //initial states
    agent0.state.obj_in_range = false; //initial states
    agent0.state.has_right_of_way = false; //initial states
    agent0.state.safe_to_enter = false; //initial states
    agent0.state.cars_waiting_to_enter = false; //initial states
    agent0.state.car_entering_range = false; //initial states
    agent0.state.obj_behind_intersection = false; //initial states
    agent0.state.is_tailgating = false; //initial states
    agent0.state.next_to_go = false; //initial states


    // Agent1 Information:
    EnvironmentAgent agent1 = agents->agents_array[1];
    agent1.id = 1;
    klee_make_symbolic( &agent1.pos_x, sizeof(float), "pos_x");
    klee_make_symbolic( &agent1.pos_z, sizeof(float), "pos_z");
    klee_make_symbolic( &agent1.angle, sizeof(float), "angle");
    klee_make_symbolic( &agent1.forward_step, sizeof(float), "forward_step");
    klee_make_symbolic( &agent1.lookahead, sizeof(float), "lookahead");
    klee_make_symbolic( &agent1.signal_choice, sizeof(TurnChoice), "signal_choice");
    klee_make_symbolic( &agent1.turn_choice, sizeof(TurnChoice), "turn_choice");
    klee_make_symbolic( &agent1.initial_direction, sizeof(Direction), "initial_direction");
    klee_make_symbolic( &agent1.intersection_arrival, sizeof(int), "intersection_arrival");
    klee_make_symbolic( &agent1.patience, sizeof(int), "patience");
    klee_make_symbolic( &agent1.step_count, sizeof(int), "step_count");
    klee_assume( agent1.pos_x == 1.316 ); // Concrete Val 
    klee_assume( agent1.pos_z == 0.499 ); // Concrete Val 
    klee_assume( agent1.angle == 4.712 ); // Concrete Val 
    klee_assume( agent1.forward_step == 0.45 ); // Concrete Val 
    klee_assume( agent1.signal_choice == "Left" ); // Concrete Val 
    klee_assume( agent1.turn_choice == "Left" ); // Concrete Val 
    klee_assume( agent1.initial_direction == 1 ); // Concrete Val 
    klee_assume( agent1.intersection_arrival == -1); // Concrete Val 
    klee_assume( agent1.lookahead == 0.585); // Concrete Val 
    agent1.prev_pos_z = agent1.pos_x; // Calculated Variable
    agent1.prev_pos_z = agent1.pos_z; // Calculated Variable
    agent1.direction = get_direction(agent1.angle/3.14*180); // Calculated Variable
    TilePos *agent1_tile_pos = get_tile_pos(agent1.pos_x, agent1.pos_z, info->road_tile_size); // Calculated Variable
    agent1.tile_x = agent1_tile_pos->x; // Calculated Variable
    agent1.tile_z = agent1_tile_pos->z; // Calculated Variable
    StopPos *agent1_stop_pos = get_stop_pos(agent1.tile_x, agent1.tile_z, info->road_tile_size, agent1.direction, agent1.speed); // Calculated Variable
    agent1.stop_x = agent1_stop_pos->x; // Calculated Variable
    agent1.stop_z = agent1_stop_pos->z; // Calculated Variable
    agent1.exists = true; // exist 

    agent1.state.in_intersection = false; //initial states
    agent1.state.at_intersection_entry = false; //initial states
    agent1.state.intersection_empty = false; //initial states
    agent1.state.approaching_intersection = false; //initial states
    agent1.state.obj_in_range = false; //initial states
    agent1.state.has_right_of_way = false; //initial states
    agent1.state.safe_to_enter = false; //initial states
    agent1.state.cars_waiting_to_enter = false; //initial states
    agent1.state.car_entering_range = false; //initial states
    agent1.state.obj_behind_intersection = false; //initial states
    agent1.state.is_tailgating = false; //initial states
    agent1.state.next_to_go = false; //initial states


    // Agent2 Information:
    EnvironmentAgent agent2 = agents->agents_array[2];
    agent2.id = 2;
    klee_make_symbolic( &agent2.pos_x, sizeof(float), "pos_x");
    klee_make_symbolic( &agent2.pos_z, sizeof(float), "pos_z");
    klee_make_symbolic( &agent2.angle, sizeof(float), "angle");
    klee_make_symbolic( &agent2.forward_step, sizeof(float), "forward_step");
    klee_make_symbolic( &agent2.lookahead, sizeof(float), "lookahead");
    klee_make_symbolic( &agent2.signal_choice, sizeof(TurnChoice), "signal_choice");
    klee_make_symbolic( &agent2.turn_choice, sizeof(TurnChoice), "turn_choice");
    klee_make_symbolic( &agent2.initial_direction, sizeof(Direction), "initial_direction");
    klee_make_symbolic( &agent2.intersection_arrival, sizeof(int), "intersection_arrival");
    klee_make_symbolic( &agent2.patience, sizeof(int), "patience");
    klee_make_symbolic( &agent2.step_count, sizeof(int), "step_count");
    klee_assume( agent2.pos_x == 1.609 ); // Concrete Val 
    klee_assume( agent2.pos_z == 2.65 ); // Concrete Val 
    klee_assume( agent2.angle == 1.571 ); // Concrete Val 
    klee_assume( agent2.forward_step == 0.51 ); // Concrete Val 
    klee_assume( agent2.signal_choice == "Left" ); // Concrete Val 
    klee_assume( agent2.turn_choice == "Left" ); // Concrete Val 
    klee_assume( agent2.initial_direction == 0 ); // Concrete Val 
    klee_assume( agent2.intersection_arrival == -1); // Concrete Val 
    klee_assume( agent2.lookahead == 0.585); // Concrete Val 
    agent2.prev_pos_z = agent2.pos_x; // Calculated Variable
    agent2.prev_pos_z = agent2.pos_z; // Calculated Variable
    agent2.direction = get_direction(agent2.angle/3.14*180); // Calculated Variable
    TilePos *agent2_tile_pos = get_tile_pos(agent2.pos_x, agent2.pos_z, info->road_tile_size); // Calculated Variable
    agent2.tile_x = agent2_tile_pos->x; // Calculated Variable
    agent2.tile_z = agent2_tile_pos->z; // Calculated Variable
    StopPos *agent2_stop_pos = get_stop_pos(agent2.tile_x, agent2.tile_z, info->road_tile_size, agent2.direction, agent2.speed); // Calculated Variable
    agent2.stop_x = agent2_stop_pos->x; // Calculated Variable
    agent2.stop_z = agent2_stop_pos->z; // Calculated Variable
    agent2.exists = true; // exist 

    agent2.state.in_intersection = false; //initial states
    agent2.state.at_intersection_entry = false; //initial states
    agent2.state.intersection_empty = false; //initial states
    agent2.state.approaching_intersection = false; //initial states
    agent2.state.obj_in_range = false; //initial states
    agent2.state.has_right_of_way = false; //initial states
    agent2.state.safe_to_enter = false; //initial states
    agent2.state.cars_waiting_to_enter = false; //initial states
    agent2.state.car_entering_range = false; //initial states
    agent2.state.obj_behind_intersection = false; //initial states
    agent2.state.is_tailgating = false; //initial states
    agent2.state.next_to_go = false; //initial states


     //Setting agent states
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.in_intersection = in_intersection(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.at_intersection_entry = at_intersection_entry(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.intersection_empty = intersection_empty(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.approaching_intersection = approaching_intersection(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.obj_in_range = object_in_range(info, i, 1);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.has_right_of_way = has_right_of_way(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.next_to_go = next_to_go(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.safe_to_enter = safe_to_enter(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.cars_waiting_to_enter = cars_waiting_to_enter(info, i);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.car_entering_range = car_entering_range(info, i, 1);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.obj_behind_intersection = car_entering_range(info, i, 1);
     }
    for(int i = 0; i < agents->num_agents; i++){
        agents->agents_array[i].state.is_tailgating = is_tailgating(info, i);
     }
}
