#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "chain.h"

/***************************************************/

tchain* tn_new(void){
    tchain* h;
    if( (h=(tchain*)malloc(sizeof(tchain))) == NULL ){
        printf("FatalError: require memory fail while creating new tnode\n");
        exit(0);
    }
    h->start = NULL ;
    h->end = NULL ;
    h->min = NULL ;
    h->max = NULL ;
    h->len = 0 ;
    return h;
}

int tn_add(tchain* self, int val, int idx){
    if( self->len < idx ) return 0;
    tnode *p,*s;
    //printf("self->len: %d, val: %d, idx: %d\n", self->len, val, idx);
    if( 0 == idx ){
        if( (s=(tnode*)malloc(sizeof(tnode))) == NULL ) return 0;
        s->val = val;
        s->next = self->start;
        self->start = s;
    }else if ( -1 == idx || self->len == idx ){
        if( (s=(tnode*)malloc(sizeof(tnode))) == NULL ) return 0;
        s->val = val;
        s->next = NULL;
        if(self->end != NULL){
            self->end->next = s;
        }
        self->end = s;
        if(self->start == NULL) self->start = self->end;
    }else{
        int t=0;
        p = self->start;
        while(t++<idx){
            p = p->next;
        }
        if( (s=(tnode*)malloc(sizeof(tnode))) == NULL ) return 0;
        s->val = val;
        s->next = p->next;
        p->next = s;
    }
    
    self->len ++;
    //printf("self->len: %d, val: %d, idx: %d\n", self->len, val, idx);
    if(self->max != NULL && self->max->val < s->val) self->max = s;
    if(self->min != NULL && self->min->val > s->val) self->min = s;
    
    return 1;
}

int tn_pop(tchain* self, int idx){
    //printf("idx: %d, ", idx);
    if( self->len < idx || (idx == 0 && self->len == 0) ) return 0;
    tnode *p,*pp;
    int v;
    if( 0 == idx ){
        p = self->start;
        self->start = p->next;
        v = p->val;
    }else{
        if( -1 == idx ) idx = self->len;
        int t=0;
        p = self->start;
        while( t++ < idx){
            pp = p;             // prevent p
            //printf("[loop] p->val: %d\n", p->val);
            p = p->next;
        }
        v = p->val;
        free(pp->next);
        pp->next = p->next;
    }
    if(self->len > 0) self->len --;
    //printf("self->len: %d,   v: %c\n", self->len, v);
    //printf(" p->val: %d\n", p->val);
    //return p->val;
    return v;
}

int tn_dump(tchain* self){
    tnode* p;
    int deep=0;
    printf("tchain info:\n\tlen: %d\n", self->len);
    if( self->start != NULL) printf("\tstart: %d\n", self->start->val);
    if( self->end != NULL) printf("\tend: %d\n", self->end->val);
    printf("tchain values:\n");
    if( (p = self->start) != NULL ){
        while(p != NULL){
            printf("\t[ %d ] %d\n", deep++, p->val);
            p = p->next;
        }
    }
    return 1;
}

int tn_len(tchain* self){
    return self->len;
}

int tn_min(tchain* self){
    if(self->min == NULL){
        return -1;
    }else{
        return self->min->val;
    }
}

int tn_max(tchain* self){
    if(self->max == NULL){
        return -1;
    }else{
        return self->max->val;
    }
}
