#include <stdbool.h>
#include <stdlib.h>

typedef enum {
    NO_ACTION = 0,
    STOP = 1,
    FORWARD_STEP = 2,
    INTERSECTION_STOP = 3,
    INTERSECTION_FORWARD = 4
} Action ;

typedef enum {
    NORTH = 0,
    SOUTH = 1,
    EAST = 2,
    WEST = 3,
} Direction ;

typedef enum {
    STRAIGHT = 0,
    LEFT = 1,
    RIGHT = 2,
    RANDOM = 3,
} TurnChoice ;

typedef struct {
    int x;
    int z;
} TilePos ;

TilePos *make_TilePos(int x, int z)
{
    TilePos *p;
    TilePos initial = {x, z};
    p = malloc(sizeof(TilePos));
    *p = initial;

    return p;
}

void free_TilePos(TilePos *p)
{
    free(p);
}

typedef struct {
    float x;
    float z;
} StopPos ;

StopPos *make_StopPos(float x, float z)
{
    StopPos *p;
    StopPos initial = {x, z};
    p = malloc(sizeof(StopPos));
    *p = initial;

    return p;
}

void free_StopPos(StopPos *p)
{
    free(p);
}


typedef struct {
    TurnChoice turn_choice;
    TurnChoice signal_choice;
    Action action;
} IntersectionAction ;

IntersectionAction *make_action(TurnChoice turn_choice, TurnChoice signal_choice, Action action)
{
    IntersectionAction *p;
    IntersectionAction initial = {turn_choice, signal_choice, action};
    p = malloc(sizeof(IntersectionAction));
    *p = initial;

    return p;
}

void free_point(IntersectionAction *p)
{
    free(p);
}

// Agent State 
typedef struct {
    bool in_intersection ;
    bool at_intersection_entry ;
    bool intersection_empty ;
    bool approaching_intersection ;
    bool obj_in_range ;
    bool has_right_of_way ;
    bool safe_to_enter ;
    bool cars_waiting_to_enter ;
    bool car_entering_range ;
    bool obj_behind_intersection ;
    bool is_tailgating ;
    bool next_to_go ;
} AgentState ;

// Environment State
typedef struct {
    int id ;
    float pos_x ;
    float pos_z ;
    float prev_pos_x ;
    float prev_pos_z ;
    float stop_x ;
    float stop_z ;
    int tile_x ;
    int tile_z ;
    float angle ;
    float speed ;
    float forward_step ;
    Direction direction ;
    Direction initial_direction ;
    TurnChoice signal_choice ;
    TurnChoice turn_choice ;
    int intersection_arrival ;
    int patience ;
    int step_count ;
    float lookahead ;
    AgentState state ;
    float q_table[1024][2];
    bool exists ;
} EnvironmentAgent ;

typedef struct {
    int num_agents;
    EnvironmentAgent agents_array[8];
} EnvironmentAgentArray ;

// Environment Info
typedef struct {
    int intersection_x ;
    int intersection_z ;
    float robot_length ;
    int grid_w ;
    int grid_h ;
    float road_tile_size ;
    int max_steps ;
    EnvironmentAgentArray agents ;
} EnvironmentInfo ;