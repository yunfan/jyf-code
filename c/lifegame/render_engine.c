#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "render_engine.h"

#define DEPTH 32

render_sdl * render_sdl_init(   int world_width, int world_height,
                                int cell_width, int cell_height,
                                int color_size, render_color * colors){
    int i;
    render_sdl * rs;

    rs = (render_sdl *)malloc(sizeof(render_sdl));
    rs->world_width = world_width;
    rs->world_height = world_height;
    rs->cell_width = cell_width;
    rs->cell_height = cell_height;

    if (SDL_Init(SDL_INIT_VIDEO) < 0 ) return NULL;
    /**
    if (!(rs->screen = SDL_SetVideoMode(cell_width*world_width,
        cell_height*world_height, DEPTH, SDL_FULLSCREEN|SDL_HWSURFACE)))
    /**/
    if (!(rs->screen = SDL_SetVideoMode(cell_width*world_width,
        cell_height*world_height, DEPTH, SDL_DOUBLEBUF)))
    {
        SDL_Quit();
        return NULL;
    }

    rs->color_index = (color_index *)malloc(sizeof(color_index));
    rs->color_index->size = color_size;
    rs->color_index->colors = (Uint32 *)calloc(color_size, sizeof(Uint32));
    rs->rects = (SDL_Rect *)calloc(world_height*world_width,
                                    sizeof(SDL_Rect));

    for(i=0; i<color_size; i++){
        *(rs->color_index->colors+i) = SDL_MapRGB(   rs->screen->format,
                                                    (colors+i)->r,
                                                    (colors+i)->g,
                                                    (colors+i)->b );
    }

    return rs;
}

void render_sdl_draw(render_sdl * rs, events * evts){
    int i;
    SDL_Rect * rect;
    event * evt;

    evt = evts->events;

    if(SDL_MUSTLOCK(rs->screen))
    {
        if(SDL_LockSurface(rs->screen) < 0) return;
    }

    rect = rs->rects;
    for(i=0; i<evts->length; i++, rect++, evt++){
        rect->x = evt->x * rs->cell_width;
        rect->y = evt->y * rs->cell_height;
        rect->w = rs->cell_width;
        rect->h = rs->cell_height;

        /**
            printf("event (%d, %d, %s)\n",
                        evt->x, evt->y,
                        evt->alive?"True":"False");
        /**/

        SDL_FillRect(   rs->screen, rect, *(rs->color_index->colors +
                        evt->alive));
    }

    if(SDL_MUSTLOCK(rs->screen)) SDL_UnlockSurface(rs->screen);
    SDL_Flip(rs->screen);
}

void render_sdl_step(void){
    SDL_Event event;

    SDL_PollEvent(&event);

    switch (event.type)
    {
        case SDL_QUIT:
            SDL_Quit();
        case SDL_KEYDOWN:
            SDL_Quit();
    }
}
