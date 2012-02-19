#include <stdio.h>
#include "core_engine.h"
#include "render_engine.h"

#define CELL_W 6
#define CELL_H 6
#define MAX_STEP 9999

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
    render_color colors[2];

    world * w;
    events * evts;
    event * evt_chain;
    render_sdl * rs;

    w = world_init(x, y);
    draw_glider(w, 1, 1);

    colors[0].r = 0;
    colors[0].g = 0;
    colors[0].b = 0;

    colors[1].r = 255;
    colors[1].g = 0;
    colors[1].b = 0;

    rs = render_sdl_init(x, y, CELL_W, CELL_H, 2, colors);

    for(step=0; step<MAX_STEP; step++, idx=0){
        evts = world_runonce(w);
        evt_chain = evts->events;

        //render_sdl_step();
        /* */
        while(idx++ < evts->length){
            printf("step %d event (%d, %d, %s)\n", step,
                        evt_chain->x, evt_chain->y,
                        evt_chain->alive?"True":"False");
            evt_chain ++ ;
        }
        /* */

        render_sdl_draw(rs, evts);
    }
    SDL_Quit();
}
