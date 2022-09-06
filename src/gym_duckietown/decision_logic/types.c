typedef enum {
    NO_ACTION = 0,
    STOP = 1,
    SLOW_DOWN = 2,
    FORWARD_STEP = 3,
    INTERSECTION_STOP = 4,
    INTERSECTION_FORWARD = 5,
    INTERSECTION_LEFT = 6,
    INTERSECTION_RIGHT = 7,
    OBSTACLE_STOP = 8,
    OBSTACLE_LEFT = 9,
    OBSTACLE_RIGHT = 10
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
    TurnChoice turn_choice;
    TurnChoice signal_choice;
    Action action;
    int num_ahead ;
} IntersectionAction ;

IntersectionAction *make_action(TurnChoice turn_choice, TurnChoice signal_choice, Action action, int num_ahead)
{
    IntersectionAction *p;
    IntersectionAction initial = {turn_choice, signal_choice, action, num_ahead};
    p = malloc(sizeof(IntersectionAction));
    *p = initial;

    return p;
}

void free_point(IntersectionAction *p)
{
    free(p);
}

typedef struct {
    float pos_x ;
    float pos_z ;
    float angle ;
    float distance_away ;
    Direction direction ;
    int intersection_arrival ;
} EnvironmentAgent ;

typedef struct {
    int elements;
    EnvironmentAgent* ENV_AGENT_ARRAY;
} EnvironmentAgentArray ;
