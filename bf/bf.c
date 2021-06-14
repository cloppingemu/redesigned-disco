#include <stdio.h>
#include <stdlib.h>

#define IO_BUF_SIZE 1024

void clean(char* code, char* cleaned){
    int input = 0;
    int output = 0;

    while (*(code+input) != '\0'){
        if ((*(code+input) == '>') | (*(code+input) == '<') |
            (*(code+input) == '+') | (*(code+input) == '-') |
            (*(code+input) == '.') | (*(code+input) == ',') |
            (*(code+input) == '[') | (*(code+input) == ']')){
                *(cleaned+output) = *(code+input);
                output++;
            }
        input++;
    }
}

int process(char* code, int* buffer, int* buffer_index, void (*output_func)(int s), int (*input_func)(void)){
    // Returns exit code
    // 0: successful execution
    // 1: Accessing out of bounds memory: over run
    // 2: Accessing out of bounds memory: under run
    // 3: Invalid instruction block: could not find block beginning
    // 3: Invalid instruction block: could not find block ending
    int code_index = 0;
    int bracket_depth = 0;

    while(*(code + code_index) != '\0'){
        switch (*(code + code_index))
        {
        case '>':
            (*buffer_index)++;
            code_index++;
            break;
        case '<':
            (*buffer_index)--;
            code_index++;
            break;
        case '+':
            (*(buffer + *buffer_index))++;
            code_index++;
            break;
        case '-':
            (*(buffer + *buffer_index))--;
            code_index++;
            break;
        case '[':
        // If current pointer occupant is not True, move to end of block
        // and then next. Otherwise, continue.
            if (!(*(buffer + *buffer_index))){
                bracket_depth--;
                while (bracket_depth != 0){
                    code_index++;
                    if (*(code + code_index) == '['){
                        bracket_depth++;
                    } else if (*(code + code_index) == ']'){
                        bracket_depth--;
                    }
                }
            }
            code_index++;
            break;
        case ']':
        // Move pointer to begining of the current block.
            bracket_depth++;
            while (bracket_depth != 0){
                code_index--;
                if (*(code + code_index) == ']'){
                    bracket_depth++;
                } else if (*(code + code_index) == '['){
                    bracket_depth--;
                }
            }
            break;
        case '.':
            output_func(*(buffer + *buffer_index));
            break;
        case ',':
            *(buffer + *buffer_index) = input_func();
            break;
        default:
            break;
        }
    }
    return 0;
}

void test_input(int (*input_func)(void)){
    int input =  input_func();
    if (input == IO_BUF_SIZE){
        puts("PASS");
    } else{
        puts("FAIL");
    }
}

void test_output(void (*output_func)(int s)){
    int num = IO_BUF_SIZE;
    output_func(num);
}
