#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void itoa(int n, char* s);

int main(int argc, char** argv){
    int i = 213443;
    char s[16];
    char* ss;
    clock_t start, finish;
    double duration;
    

    start = clock();
    /** **/
    for(i=1; i<=1000000; i++){
        ss = s;
        itoa(i, ss);
    }
    /** **
    ss = s;
    itoa(1003, ss);
    /** **/
    
    finish = clock();

    duration = (double)(finish - start)/CLOCKS_PER_SEC;

    printf("duration: %f sec\n", duration);
    
    printf("%d ==> %s\n", i-1, ss);
    
    return 0;
}

void itoa(int i, char* s){
    //char* ss = s;
    int power, j;

    //printf("%d = ", i);

    j = i;
    for(power=1; j>=10; j/=10)
        power *= 10;
    
    //printf("power: %d\n", power);

    for(;power>0;power/=10){
        *s++ = '0' + i/power;
        i %= power;
    }

    *s = '\0';
    //printf("ss = %s\n", ss);
}
