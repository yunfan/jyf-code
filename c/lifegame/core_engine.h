#ifndef __CORE_ENGINE
#define __CORE_ENGINE
#define TRUE 1
#define FALSE 0

/* cell type */
typedef struct {
    unsigned alive:1;
    unsigned :27;           /* for 32bit machine this pad field should be
                                32 - 5 = 27 */
    unsigned brother:4;
} cell;

/* event type */
typedef struct {
    unsigned x:15;
    unsigned y:15;
    unsigned :1;        /* pad field */
    unsigned alive:1;
} event;

/* events type */
typedef struct {
    unsigned int length;
    event * events;
} events;

/* world type */
typedef struct {
    unsigned int width;
    unsigned int height;
    unsigned int alive_count;
    cell * cells;
    events * evts;
} world;


/* world operation */
world * world_init(unsigned int width, unsigned int height);

void world_set_cell(world * w, unsigned int x, unsigned int y, int alive);

events * world_runonce(world * w);

void events_free(events * evts);

#endif
