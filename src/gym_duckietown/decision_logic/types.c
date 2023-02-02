#include <stdbool.h>
#include <stdlib.h>
#include "types.h"

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
