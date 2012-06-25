#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "chain.h"

int frand(int start, int end);
void mixit(char* s);

int frand(int start, int end){
    if(start >= end ) return 0;
    return (int)( (double)rand() / (double)(RAND_MAX + 1.0) * (double)(end - start) + start );
    //return (int)( (double)rand() / (double)(RAND_MAX + 1) * (double)(end - start) + start );
}


int main(int argc, char* argv[]){
    int i ;
    for(i=1; i<argc; i++){
        printf("now process %s \n", argv[i]);
        mixit(argv[i]);
    }
    return 0;
}

void mixit(char* s){
    tchain* tmp;
    char c;
    char cs[99];
    char* csp;
    int loc,idx,i;
    tnode p;
    
    //printf("mixit init done\n");   
    tmp = tn_new();
    csp = cs;
    printf("Target: %s\n", s);
    while( ( c = *s++ ) ){
        tn_add(tmp, c, -1);
    }
    //tn_dump(tmp);
    printf("Target init done\n");

    srand(time(NULL));
    while(tmp->len > 1){
        loc = frand(1,tmp->len);
        //printf("now loc = %d, tmp->length = %d\n", loc, tmp->len);
        c = tn_pop(tmp,loc);
        if( 0 == c ){
            printf("error now\n");
            exit(0);
        }else{
            *csp++ = c;
        }
    }
    printf("Length: %d \n", csp - cs);
    *csp++ = tmp->start->val;
    *csp = 0;
    printf("\n");
    idx = 0;
    while( (c = cs[idx++]) ){
        printf("%c",c);
    }
    printf("\nok\n");
}

