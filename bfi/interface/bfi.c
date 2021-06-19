#include <stdio.h>
#include <stdlib.h>
#include <bf.h>

#define IO_BUF_SIZE 256

#define INPUT_PROMPT " : "
#define INPUT_BUF_SIZE 4096
#define INTERFACE_BUF_SIZE 4096

void output_func_int(int i){
    char snum[IO_BUF_SIZE]; 
    sprintf(snum, "%d", i);
    puts(snum);
}

void output_func_ascii(int c){
    putc(c, stdout);
}

int input_func_ascii(void){
    char buf[IO_BUF_SIZE] = {0};
    fputs(" ascii: ", stdout);
    fgets(buf, IO_BUF_SIZE, stdin);
    return (int) *buf;
}

int all_numeric(char* s){
    int i = 0;
    while (*(s+i) != '\0'){
        if (((*(s+i)) < '0') | ((*(s+i)) > '9')){
            return 0;
        }
        i++;
    }
    return 1;
}

int main(void){
    char input[INPUT_BUF_SIZE] = {[0 ... 1023] = 1};
    char code[INPUT_BUF_SIZE];
    int buffer[INTERFACE_BUF_SIZE];
    int buffer_index;

    while (!(((*input) == 'q') & ((*(input+1)) == '\n'))){
        clean(input, code);
        process(code, buffer, &buffer_index, output_func_int, input_func_ascii);
        fputs(INPUT_PROMPT, stdout);
        fgets(input, INPUT_BUF_SIZE, stdin);
    }
    return 0;
}
