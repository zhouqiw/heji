/* File: example.c */

#include "example.h"
#include <stdio.h>

int fact(int n) {
    if (n < 0){ /* This should probably return an error, but this is simpler */
        return 0;
    }
    if (n == 0) {
        return 1;
    }
    else {
        /* testing for overflow would be a good idea here */
        return n * fact(n-1);
    }
}

int sum(int  m ) {
    if (m <= 0 ){
        return 0 ;
    }
    if (m == 1){
        return 1;
    } else {
        int s = 0;
        for (int i = 0 ; i < m+1  ; i++)
        {   printf(" %d",s);
            s = s + i;
//            printf("+ %d =  %d   ",i,s);
//            if(s%10 == 0){
//              printf("\n");  
//            }
        }
        printf("sum= %d\n",s);
        return s;
    }
    
}

int sum1(int l){
    return l*l;
}
