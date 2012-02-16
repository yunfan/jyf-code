#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "core_engine.h"

world * world_init(unsigned int width, unsigned int height){
    world * w;
    int total, offset;

    total = width * height;

    w = (world *)malloc(sizeof(world));
    w->width = width;
    w->height = height;
    w->alive_count = 0;
    w->cells = (cell *)calloc(total, sizeof(cell));

    return w;
}

static unsigned int world_get_offset(world * w, unsigned int x, unsigned int
y);
static unsigned int world_get_offset(world * w, unsigned int x, unsigned int
y){
    return (y%(w->height))*(w->width) + x % (w->width);
}

void world_set_cell(world * w, unsigned int x, unsigned int y, int alive){
    int offset;
    int plus;

    offset = y * (w->width) + x;
    plus = alive ? 1:-1;

    (w->cells+offset)->alive = alive;
    (w->alive_count) += plus ;

    /* update top-left, top-midle, top-right */
    (w->cells+world_get_offset(w, x-1, y-1))->brother += plus;
    (w->cells+world_get_offset(w, x, y-1))->brother += plus;
    (w->cells+world_get_offset(w, x+1, y-1))->brother += plus;

    /* update midle-left, middle-right  */
    (w->cells+world_get_offset(w, x-1, y))->brother += plus;
    (w->cells+world_get_offset(w, x+1, y))->brother += plus;

    /* update bottom-left, bottom-middle, bottom-right  */
    (w->cells+world_get_offset(w, x-1, y+1))->brother += plus;
    (w->cells+world_get_offset(w, x, y+1))->brother += plus;
    (w->cells+world_get_offset(w, x+1, y+1))->brother += plus;

}

events * world_runonce(world * w){
    int total, offset, x, y;
    int keep_on, alive;
    events * evt;

    cell * old_cells;

    total = (w->width) * (w->height);

    old_cells = (cell *)calloc(total, sizeof(cell));
    evt = (events *)malloc(sizeof(events));
    evt->length = 0;
    evt->events = (event *)calloc(total, sizeof(event));

    memcpy(old_cells, w->cells, total);

    for(y=0; y<w->height; y++){
        for(x=0; x<w->width; x++){
            if((old_cells->alive) && (old_cells->brother<2 || old_cells->brother>3)){
                /* *
                printf("[%d, %d] alive = %d, brother = %d\n", x, y,
                            old_cells->alive, old_cells->brother);
                /* */
                keep_on = TRUE;
                alive = FALSE;
            }else if (!old_cells->alive && (old_cells->brother == 3)){
                /* *
                printf("[%d, %d] alive = %d, brother = %d\n", x, y,
                            old_cells->alive, old_cells->brother);
                /* */
                keep_on = TRUE;
                alive = TRUE;
            }

            if(keep_on){
                evt->events->x = x;
                evt->events->y = y;
                evt->events->alive = alive;
                evt->events++;
                evt->length++;
                world_set_cell(w, x, y, alive);
            }
            old_cells ++ ;
            keep_on = FALSE;
        }
    }
    evt->events -= evt->length;

    return evt;
}
