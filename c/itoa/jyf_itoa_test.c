#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX (1<<31-1)
int get_dec_power(int n);
char* jyf_itoa(int n, char* s);

int b2d[10] = { 0,
        10,
        100,
        1000,
        10000,
        100000,
        1000000,
        10000000,
        100000000,
        1000000000
};

int main(int argc, char** argv){
    int i = 213443;
    char* s, *ss;
    clock_t start, finish;
    double duration;
    
    s = (char*)malloc(sizeof(char)*16);
    start = clock();
    for(i=1;i<=1000000;i++)
        ss = jyf_itoa(i, s);
    finish = clock();

    duration = (double)(finish - start)/CLOCKS_PER_SEC;

    printf("duration: %f sec\n", duration);
    if( ss != NULL)
        printf("%d ==> %s\n", i-1, ss);
    else
        printf("atoi fail\n");

    return 0;
}

char* jyf_itoa(int n, char* s){
    if ( n > MAX ) {
        //printf("%d > %d fail\n", n, MAX);
        return NULL;
    }

    char dec_power;
    int power;
    dec_power = get_dec_power(n);

    s += dec_power + 1;
    *s-- = '\0';

    for(;dec_power>0;dec_power--){
        *s-- = '0' + n%10;
        n /= 10;
    }
    *s = '0';
    //printf("now string is %s\n", s);
    return s;
}

int get_dec_power(int n){
    if ( n > MAX )
        return -1;

    if (n >= b2d[7])
        if (n >= b2d[9])
            return 10;
        else if (n >= b2d[8])
            return 9;
        else
            return 8;

    char idx=4, wid = 2;

    while (wid > 0){
        if (n > b2d[idx])
            idx += wid;
        else if (n < b2d[idx])
            idx -= wid;
        else
            return idx + 1;

        wid /= 2;

    }

    if (n >= b2d[idx])
        return idx + 1;
    else
        return idx -1 + 1;
}
