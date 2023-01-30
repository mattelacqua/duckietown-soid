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
    EnvironmentAgentArray *agents = malloc(sizeof(EnvironmentAgent) * 3);

    // Agent0 Information:
    EnvironmentAgent *agent0 = malloc(sizeof(EnvironmentAgent));
    agent0->id = 0;
    klee_make_symbolic( &agent0->pos_x, sizeof(float), "pos_x");
    klee_make_symbolic( &agent0->pos_z, sizeof(float), "pos_z");
    klee_make_symbolic( &agent0->angle, sizeof(float), "angle");
    klee_make_symbolic( &agent0->forward_step, sizeof(float), "forward_step");
    klee_make_symbolic( &agent0->lookahead, sizeof(float), "lookahead");
    klee_assume( agent0->pos_x == 2.476 ); // Concrete Val 
    klee_assume( agent0->pos_z == 1.316 ); // Concrete Val 
    klee_assume( agent0->angle == 3.142 ); // Concrete Val 
    klee_assume( agent0->forward_step == 0.51 ); // Concrete Val 
    klee_assume( agent0->speed == None ); // Concrete Val 
    klee_assume( agent0->turn_choice == "Straight" ); // Concrete Val 
    klee_assume( agent0->lookahead == 0.585); // Concrete Val 
    klee_assume( agent0->speed > 0.52 && agent0->speed < 0.513);
    agents->agents_array[0] = *agent0;
    agents->num_agents += 1;

    // Agent1 Information:
    EnvironmentAgent *agent1 = malloc(sizeof(EnvironmentAgent));
    agent1->id = 1;
    klee_make_symbolic( &agent1->pos_x, sizeof(float), "pos_x");
    klee_make_symbolic( &agent1->pos_z, sizeof(float), "pos_z");
    klee_make_symbolic( &agent1->angle, sizeof(float), "angle");
    klee_make_symbolic( &agent1->forward_step, sizeof(float), "forward_step");
    klee_make_symbolic( &agent1->lookahead, sizeof(float), "lookahead");
    klee_assume( agent1->pos_x == 2.839 ); // Concrete Val 
    klee_assume( agent1->pos_z == 1.316 ); // Concrete Val 
    klee_assume( agent1->angle == 3.142 ); // Concrete Val 
    klee_assume( agent1->forward_step == 0.45 ); // Concrete Val 
    klee_assume( agent1->speed == 0 ); // Concrete Val 
    klee_assume( agent1->turn_choice == "Left" ); // Concrete Val 
    klee_assume( agent1->lookahead == 0.585); // Concrete Val 
    agents->agents_array[1] = *agent1;
    agents->num_agents += 1;

    // Agent2 Information:
    EnvironmentAgent *agent2 = malloc(sizeof(EnvironmentAgent));
    agent2->id = 2;
    klee_make_symbolic( &agent2->pos_x, sizeof(float), "pos_x");
    klee_make_symbolic( &agent2->pos_z, sizeof(float), "pos_z");
    klee_make_symbolic( &agent2->angle, sizeof(float), "angle");
    klee_make_symbolic( &agent2->forward_step, sizeof(float), "forward_step");
    klee_make_symbolic( &agent2->lookahead, sizeof(float), "lookahead");
    klee_assume( agent2->pos_x == 1.316 ); // Concrete Val 
    klee_assume( agent2->pos_z == 0.31 ); // Concrete Val 
    klee_assume( agent2->angle == 4.712 ); // Concrete Val 
    klee_assume( agent2->forward_step == 0.51 ); // Concrete Val 
    klee_assume( agent2->speed == 0 ); // Concrete Val 
    klee_assume( agent2->turn_choice == "Right" ); // Concrete Val 
    klee_assume( agent2->lookahead == 0.585); // Concrete Val 
    agents->agents_array[2] = *agent2;
    agents->num_agents += 1;
}
