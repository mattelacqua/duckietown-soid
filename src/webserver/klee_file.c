#include "src/gym_duckietown/decision_logic/types.c"
int main(int argc, char **argv) {
EnvironmentInfo *info = malloc(sizeof(EnvironmentInfo));
klee_open_merge();
info->intersection_x = 2;
info->intersection_z = 2;
info->robot_length = 0.18;
info->grid_w = 5;
info->grid_h = 5;
info->road_tile_size = 0.585;
info->max_steps = 1500;
EnvironmentAgentArray *agents = malloc(sizeof(EnvironmentAgent) * 3);
EnvironmentAgent *agent0 = malloc(sizeof(EnvironmentAgent));
agent0->id = 0;
klee_make_symbolic( &agent0->pos_x, sizeof(float), "pos_x");
klee_make_symbolic( &agent0->pos_z, sizeof(float), "pos_z");
klee_make_symbolic( &agent0->angle, sizeof(float), "angle");
klee_make_symbolic( &agent0->forward_step, sizeof(float), "forward_step");
klee_make_symbolic( &agent0->lookahead, sizeof(float), "lookahead");
klee_assume( agent0->pos_x == 1.609 );
klee_assume( agent0->pos_z == None );
klee_assume( agent0->angle == 1.571 );
klee_assume( agent0->forward_step == 0.51 );
klee_assume( agent0->speed == 0 );
klee_assume( agent0->direction == "Left" );
klee_assume( agent0->lookahead == 0.585);
klee_assume( agent0->direction == "Right" );
klee_assume( agent0->direction == "Left" || agent0->direction == "Straight");
klee_assume( agent0->pos_z == 1 );
agents->agents_array[0] = *agent0;
agents->num_agents += 1;
EnvironmentAgent *agent1 = malloc(sizeof(EnvironmentAgent));
agent1->id = 1;
klee_make_symbolic( &agent1->pos_x, sizeof(float), "pos_x");
klee_make_symbolic( &agent1->pos_z, sizeof(float), "pos_z");
klee_make_symbolic( &agent1->angle, sizeof(float), "angle");
klee_make_symbolic( &agent1->forward_step, sizeof(float), "forward_step");
klee_make_symbolic( &agent1->lookahead, sizeof(float), "lookahead");
klee_assume( agent1->pos_x == 1.609 );
klee_assume( agent1->pos_z == 2.839 );
klee_assume( agent1->angle == 1.571 );
klee_assume( agent1->forward_step == 0.45 );
klee_assume( agent1->speed == 0 );
klee_assume( agent1->direction == "Straight" );
klee_assume( agent1->lookahead == 0.585);
agents->agents_array[1] = *agent1;
agents->num_agents += 1;
EnvironmentAgent *agent2 = malloc(sizeof(EnvironmentAgent));
agent2->id = 2;
klee_make_symbolic( &agent2->pos_x, sizeof(float), "pos_x");
klee_make_symbolic( &agent2->pos_z, sizeof(float), "pos_z");
klee_make_symbolic( &agent2->angle, sizeof(float), "angle");
klee_make_symbolic( &agent2->forward_step, sizeof(float), "forward_step");
klee_make_symbolic( &agent2->lookahead, sizeof(float), "lookahead");
klee_assume( agent2->pos_x == 0.31 );
klee_assume( agent2->pos_z == 1.609 );
klee_assume( agent2->angle == 6.283 );
klee_assume( agent2->forward_step == 0.51 );
klee_assume( agent2->speed == 0 );
klee_assume( agent2->direction == "Left" );
klee_assume( agent2->lookahead == 0.585);
agents->agents_array[2] = *agent2;
agents->num_agents += 1;
}