#include <stdio.h>
#include "core_engine.h"

void draw_glider(world * w, unsigned int x, unsigned int y);
void draw_glider(world * w, unsigned int x, unsigned int y){
    world_set_cell(w, x, y+1, TRUE);
    world_set_cell(w, x+1, y+2 , TRUE);
    world_set_cell(w, x+2, y, TRUE);
    world_set_cell(w, x+2, y+1, TRUE);
    world_set_cell(w, x+2, y+2, TRUE);
}

int main(int argc, char * * argv){
    int x = 96;
    int y = 96;
    int idx = 0;
    int step = 0;
    world * w;
    events * evts;

    w = world_init(x, y);
    draw_glider(w, 1, 1);

    for(step=0; step<99; step++){
        evts = world_runonce(w);

        while(idx++ < evts->length){
            printf("step %d event (%d, %d, %s)\n", step,
                        evts->events->x, evts->events->y,
                        evts->events->alive?"True":"False");
            evts->events ++ ;
        }
        idx = 0 ;
    }
}
