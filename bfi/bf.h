#ifndef libbf_h__
#define libbf_h__

void clean(char* code, char* cleaned);
int process(char* code, int* buffer, int* buffer_index, void (*output_func)(int s), int (*input_func)(void));

#endif  // libbf_h__
