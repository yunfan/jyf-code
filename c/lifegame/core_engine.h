#define TRUE 1
#define FALSE 0

/* cell type */
typedef struct {
    unsigned alive:1;
    unsigned :27;           /* for 32bit machine this pad field should be
                                32 - 5 = 27 */
    unsigned brother:4;
} cell;

/* world type */
typedef struct {
    unsigned int width;
    unsigned int height;
    unsigned int alive_count;
    cell * cells;
} world;

/* event type */
typedef struct {
    unsigned int x;
    unsigned int y;
    unsigned int alive;
} event;

/* events type */
typedef struct {
    unsigned int length;
    event * events;
} events;

/* world operation */
world * world_init(unsigned int width, unsigned int height);

void world_set_cell(world * w, unsigned int x, unsigned int y, int alive);

events * world_runonce(world * w);
