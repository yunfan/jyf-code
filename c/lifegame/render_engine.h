#ifndef __RENDRE_ENGINE
#define __RENDER_ENGINE

#include <SDL/SDL.h>
#include "core_engine.h"

typedef struct {
    unsigned r:8;
    unsigned g:8;
    unsigned b:8;
} render_color;

typedef struct {
    int size;
    Uint32 * colors;
} color_index;

typedef struct{
    int world_width;
    int world_height;
    int cell_width;
    int cell_height;
    SDL_Surface * screen;
    color_index * color_index;
    SDL_Rect * rects;
} render_sdl;

render_sdl * render_sdl_init(   int world_width, int world_height,
                                int cell_width, int cell_height,
                                int color_size, render_color * colors);

void render_sdl_draw(render_sdl * render, events * evts);

void render_sdl_step(void);

#endif
