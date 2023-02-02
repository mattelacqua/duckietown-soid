#include <stdbool.h>
#include <stdlib.h>
#include "types.h"

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
