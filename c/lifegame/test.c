#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include "core_engine.h"
#include "render_engine.h"

#define CELL_W 4
#define CELL_H 4
#define MAX_STEP 1256

void draw_glider(world * w, unsigned int x, unsigned int y);
void draw_glider(world * w, unsigned int x, unsigned int y){
    world_set_cell(w, x, y+1, TRUE);
    world_set_cell(w, x+1, y+2 , TRUE);
    world_set_cell(w, x+2, y, TRUE);
    world_set_cell(w, x+2, y+1, TRUE);
    world_set_cell(w, x+2, y+2, TRUE);
}

void draw_glider_gun(world * w, unsigned int x, unsigned int y);
void draw_glider_gun(world * w, unsigned int x, unsigned int y){
    world_set_cell(w, x+1, y+5, TRUE);
    world_set_cell(w, x+1, y+6, TRUE);
    world_set_cell(w, x+2, y+5, TRUE);
    world_set_cell(w, x+2, y+6, TRUE);
    world_set_cell(w, x+2, y+6, TRUE);

    world_set_cell(w, x+11, y+5, TRUE);
    world_set_cell(w, x+11, y+6, TRUE);
    world_set_cell(w, x+11, y+7, TRUE);

    world_set_cell(w, x+12, y+4, TRUE);
    world_set_cell(w, x+12, y+8, TRUE);

    world_set_cell(w, x+13, y+3, TRUE);
    world_set_cell(w, x+13, y+9, TRUE);

    world_set_cell(w, x+14, y+3, TRUE);
    world_set_cell(w, x+14, y+9, TRUE);

    world_set_cell(w, x+15, y+6, TRUE);

    world_set_cell(w, x+16, y+4, TRUE);
    world_set_cell(w, x+16, y+8, TRUE);

    world_set_cell(w, x+17, y+5, TRUE);
    world_set_cell(w, x+17, y+6, TRUE);
    world_set_cell(w, x+17, y+7, TRUE);

    world_set_cell(w, x+18, y+6, TRUE);

    world_set_cell(w, x+21, y+3, TRUE);
    world_set_cell(w, x+21, y+4, TRUE);
    world_set_cell(w, x+21, y+5, TRUE);

    world_set_cell(w, x+22, y+3, TRUE);
    world_set_cell(w, x+22, y+4, TRUE);
    world_set_cell(w, x+22, y+5, TRUE);

    world_set_cell(w, x+23, y+2, TRUE);
    world_set_cell(w, x+23, y+6, TRUE);

    world_set_cell(w, x+25, y+1, TRUE);
    world_set_cell(w, x+25, y+2, TRUE);
    world_set_cell(w, x+25, y+6, TRUE);
    world_set_cell(w, x+25, y+7, TRUE);

    world_set_cell(w, x+35, y+3, TRUE);
    world_set_cell(w, x+35, y+4, TRUE);

    world_set_cell(w, x+36, y+3, TRUE);
    world_set_cell(w, x+36, y+4, TRUE);

}

int main(int argc, char * * argv){
    int gen_sig;
    int x = 128;
    int y = 128;
    int idx = 0;
    int step = 0;
    useconds_t i = 10000;
    render_color colors[2];

    world * w;
    events * evts;
    event * evt_chain;
    render_sdl * rs;

    w = world_init(x, y);
    //draw_glider_gun(w, 1, 1);
    //draw_glider(w, 59, 59);
    draw_glider_gun(w, 1, 1);

    colors[0].r = 0;
    colors[0].g = 0;
    colors[0].b = 0;

    colors[1].r = 255;
    colors[1].g = 0;
    colors[1].b = 0;

    rs = render_sdl_init(x, y, CELL_W, CELL_H, 2, colors);

    srand(time(NULL));

    //for(step=0; step<MAX_STEP; step++, idx=0){
    while(++step){
        evts = world_runonce(w);
        evt_chain = evts->events;

        //render_sdl_step();
        /* *
        while(idx++ < evts->length){
            printf("step %d event (%d, %d, %s)\n", step,
                        evt_chain->x, evt_chain->y,
                        evt_chain->alive?"True":"False");
            evt_chain ++ ;
        }
        //printf("step %d alive count: %d\n", step, w->alive_count);
        /* */

        render_sdl_draw(rs, evts);

        /* */
        gen_sig = rand()%100;
        if(gen_sig>95){
            printf("step %d now generate a glider\n", step);
            draw_glider(w, rand()%(w->width-5), rand()%(w->height-5));
        }
        /* */

        /* if there is no event occur, then generate a glider*
        if(!evts->length){
            printf("step %d now generate a glider\n", step);
            draw_glider(w, rand()%(w->width-5), rand()%(w->height-5));
        }
        /* */

        usleep(i);
    }
    SDL_Quit();
}
