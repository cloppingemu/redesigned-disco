#include <stdio.h>
#include <stdlib.h>

int main(void){
    char s[16] = {0};
    char* i = '\0';

    while (!s[0]){
        i = fgets(s, 8, stdin);
        puts(s);
    }

    return *i;
}
