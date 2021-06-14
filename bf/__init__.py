__author__ = "Clopping Emu"
__version__ = "0.1"

__all__ = ["clean", "process"]

import ctypes
from os.path import dirname, realpath

_so_path = "/".join((dirname(realpath(__file__)), "libbf.so"))

libbf = ctypes.cdll.LoadLibrary(_so_path)

# int (*input_func)(void)
_input_func_prototype = ctypes.CFUNCTYPE(ctypes.c_int)
# void (*output_func)(int* s)
_output_func_prototype = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int)

class BF(object):
    """
input_func: functions
output_func: functions
"""

    def __init__(self, buffer_size=256, input_func=None, output_func=None):
        self.buffer = (ctypes.c_int * buffer_size)(*[0, ] * buffer_size)
        self.buffer_position = ctypes.c_int(0)

        if input_func is None:
            self.input_func = self._input_func
        else:
            self.input_func = input_func
        if output_func is None:
            self.output_func = self._output_func
        else:
            self.output_func = output_func
    
        self.input_func = _input_func_prototype(self.input_func)
        self.output_func = _output_func_prototype(self.output_func)

    def interact(self, ):
        pass

    def process(self, code):
        libbf.process(code.encode(), ctypes.pointer(self.buffer_position), self.output_func, self.input_func)

    @staticmethod
    def _input_func() -> ctypes.c_int:
        return ord(input("ascii: ")[0])

    @staticmethod
    def _output_func(num:int) -> None:
        print(num, flush=True)

    @staticmethod
    def clean(code:str, output_buffer_size=256)->str:
        output_buffer = (ctypes.c_char * output_buffer_size)(*[0, ] * output_buffer_size)
        input_buffer = ctypes.create_string_buffer(code.encode())

        libbf.clean(input_buffer, output_buffer)

        return output_buffer.value.decode()


if __name__ == "__main__":
    s0 = """
++++++++               Set Cell #0 to 8
[
    >++++               Add 4 to Cell #1; this will always set Cell #1 to 4
    [                   as the cell will be cleared by the loop
        >++             Add 2 to Cell #2
        >+++            Add 3 to Cell #3
        >+++            Add 3 to Cell #4
        >+              Add 1 to Cell #5
        <<<<-           Decrement the loop counter in Cell #1
    ]                   Loop till Cell #1 is zero; number of iterations is 4
    >+                  Add 1 to Cell #2
    >+                  Add 1 to Cell #3
    >-                  Subtract 1 from Cell #4
    >>+                 Add 1 to Cell #6
    [<]                 Move back to the first zero cell you find; this will
                        be Cell #1 which was cleared by the previous loop
    <-                  Decrement the loop Counter in Cell #0
]                       Loop till Cell #0 is zero; number of iterations is 8

The result of this is:
Cell No :   0   1   2   3   4   5   6
Contents:   0   0  72 104  88  32   8
Pointer :   ^

>>.                     Cell #2 has value 72 which is 'H'
>---.                   Subtract 3 from Cell #3 to get 101 which is 'e'
+++++++..+++.           Likewise for 'llo' from Cell #3
>>.                     Cell #5 is 32 for the space
<-.                     Subtract 1 from Cell #4 for 87 to give a 'W'
<.                      Cell #3 was set to 'o' from the end of 'Hello'
+++.------.--------.    Cell #3 for 'rl' and 'd'
>>+.                    Add 1 to Cell #5 gives us an exclamation point
>++.                    And finally a newline from Cell #6"""
    r0 = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    print("Test suite:\n")
    print("Removing non-code test:", BF.clean(s0, 1024) == r0 and "PASS" or "FAIL")
    print("Not changing code:", BF.clean(r0, 1024) == r0 and "PASS" or "FAIL")

    def test_output_func(num): print("Recieving value to output function:", num == 1024 and "PASS" or "FAIL")
    libbf.test_output(_output_func_prototype(test_output_func))

    def test_input_func(): print("Passing value to input function: ", end="", flush=True); return 1024
    libbf.test_input(_input_func_prototype(test_input_func))

    s1 = '''
    ++       Cell c0 = 2
> +++++  Cell c1 = 5

[        Start your loops with your cell pointer on the loop counter (c1 in our case)
< +      Add 1 to c0
> -      Subtract 1 from c1
]        End your loops with the cell pointer on the loop counter

At this point our program has added 5 to 2 leaving 7 in c0 and 0 in c1
but we cannot output this value to the terminal since it is not ASCII encoded.

To display the ASCII character "7" we must add 48 to the value 7.
We use a loop to compute 48 = 6 * 8.

++++ ++++  c1 = 8 and this will be our loop counter again
[
< +++ +++  Add 6 to c0
> -        Subtract 1 from c1
]
< .        Print out c0 which has the value 55 which translates to "7"!'''
    r1 = BF.clean(s1)

    print("\nRunning program: ", r1)
    bfi = BF()
    bfi.process("+")
