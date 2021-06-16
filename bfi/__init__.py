__author__ = "Clopping Emu"
__version__ = "0.1"

import ctypes
from os.path import dirname, realpath


_so_path = "/".join((dirname(realpath(__file__)), "libbf.so"))
libbf = ctypes.cdll.LoadLibrary(_so_path)

libbf.clean.argtypes = (
    ctypes.POINTER(ctypes.c_char),  # char* code
    ctypes.POINTER(ctypes.c_char),  # char* cleaned
)

# int (*input_func)(void)
_input_func_prototype = ctypes.CFUNCTYPE(ctypes.c_int)
# void (*output_func)(int* s)
_output_func_prototype = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int)
libbf.process.argtypes = (
    ctypes.POINTER(ctypes.c_char),  # char* code
    ctypes.POINTER(ctypes.c_int),   # int* buffer
    ctypes.POINTER(ctypes.c_int),   # int* buffer_index
    _output_func_prototype,         # void (*output_func)(int* s)
    _input_func_prototype,           # int (*input_func)(void)    
)
libbf.process.restype = ctypes.c_int


class BF(object):
    """
input_func: functions
output_func: functions
"""

    def __init__(self, buffer_size=256, input_func=None, output_func=None):
        self.io_formats = ["decimal", "ascii"]
        self.io_func_mapping = {
            "ascii": {
                "input": self._input_func_ascii,
                "output": self._output_func_ascii
            },
            "decimal": {
                "input": self._input_func_decimal,
                "output": self._output_func_decimal
            }
        }

        self.buffer = (ctypes.c_int * buffer_size)(*[0, ] * buffer_size)
        self.buffer_index = ctypes.c_int(0)

        if input_func is None:
            self.input_func = self._input_func_ascii
        else:
            self.input_func = input_func
        if output_func is None:
            self.output_func = self._output_func_ascii
        else:
            self.output_func = output_func
    
        self.input_func = _input_func_prototype(self.input_func)
        self.output_func = _output_func_prototype(self.output_func)

    def interact(self, ):
        code = ""
        docstr = """
Interacting with BF interface. Available instructions are,

>\tIncrement the data pointer.
<\tDecrement the data pointer.
+\tIncrement the byte at the data pointer.
-\tDecrement the byte at the data pointer.
.\tOutput the byte at the data pointer.
,\tAccept one byte of input, storing its value in the byte at the data pointer.
[\tIf the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
]\tIf the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.

input\tSelect input type between decimal or ascii as `input [ascii]/decimal`
output\tSelect output type between decimal or ascii as `output [ascii]/decimal`
help\tPrint this message
buffer\tPrint buffer as decimal"""
        print(docstr, flush=True)
        while code != "q":
            code = input("\n: ")
            if code[:5] == "input":
                input_func = self.io_func_mapping.get(code[6:], None)
                if input_func is None:
                    print("'", code[6:], "'", "function not avaiable", flush=True)
                else:
                    self.input_func = _input_func_prototype(input_func["input"])
            elif code[:6] == "output":
                output_func = self.io_func_mapping.get(code[7:], None)
                if output_func is None:
                    print("'", code[7:], ",", "function not available", flush=True)
                else:
                    self.output_func = _output_func_prototype(output_func["output"])
            elif code[:4] == "help":
                print(docstr, flush=True)
            elif code[:6] == "buffer":
                print(list(self.buffer))
            elif code[:5] == "index":
                print(self.buffer_index.value)
            else:
                self.process(code)

    def process(self, code):
        libbf.process(self.clean(code, len(code)).encode(), self.buffer, ctypes.byref(self.buffer_index), self.output_func, self.input_func)

    @staticmethod
    def _input_func_ascii() -> ctypes.c_int:
        return ord(input("ascii: ")[0])

    @staticmethod
    def _output_func_ascii(num:int) -> None:
        print(chr(num), end="", flush=True)

    @staticmethod
    def _input_func_decimal() -> ctypes.c_int:
        return int(input("decimal: "))

    @staticmethod
    def _output_func_decimal(num:int) -> None:
        print(num, end="", flush=True)

    @staticmethod
    def clean(code:str, output_buffer_size=256)->str:
        output_buffer = (ctypes.c_char * output_buffer_size)(*[0, ] * output_buffer_size)
        input_buffer = ctypes.create_string_buffer(code.encode())

        libbf.clean(input_buffer, output_buffer)

        return output_buffer.value.decode()
