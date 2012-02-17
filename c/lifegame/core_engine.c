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

    w->evts = (events * )malloc(sizeof(events));
    w->evts->length = 0;
    w->evts->events = (event *)calloc(total, sizeof(event));

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
    int total, x, y, offset;
    int keep_on, alive;

    events * evts;
    event * evt_chain;
    cell * cells;

    total = (w->width) * (w->height);

    cells = w->cells;

    evts = w->evts;
    evts->length = 0;
    evt_chain = evts->events;

    keep_on = FALSE;

    /* detect events */
    for(y=0; y<w->height; y++){
        for(x=0; x<w->width; x++, keep_on = FALSE, cells++){
            if((cells->alive) && (cells->brother<2 || cells->brother>3)){
                keep_on = TRUE;
                alive = FALSE;
            }else if (!cells->alive && (cells->brother == 3)){
                keep_on = TRUE;
                alive = TRUE;
            }

            if(keep_on){
                evt_chain->x = x;
                evt_chain->y = y;
                evt_chain->alive = alive;                           // alive or dead
                evt_chain++;

                evts->length++;
            }
        }
    }

    /* update world */
    evt_chain = evts->events;
    for(offset=0; offset<evts->length;
        offset++,
        world_set_cell(w,
            evt_chain->x,
            evt_chain->y,
            evt_chain->alive),
        evt_chain++);

    return evts;
}

void events_free(events * evts){
    free(evts->events);
    free(evts);
}
