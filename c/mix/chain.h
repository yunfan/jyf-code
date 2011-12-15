/**************************************************************/

struct NODE {
    int val;
    struct NODE* next;
};
typedef struct NODE tnode;

struct CHAIN {
    tnode* start;
    tnode* end;
    tnode* min;
    tnode* max;
    int len;
};
typedef struct CHAIN tchain;

int frand(int start, int end);
void dump_chain(tnode* h);

tchain* tn_new(void);
int tn_add(tchain* self, int val, int idx);
int tn_pop(tchain* self, int idx);
int tn_dump(tchain* self);
int tn_len(tchain* self);
int tn_min(tchain* self);
int tn_max(tchain* self);

/**************************************************************/
