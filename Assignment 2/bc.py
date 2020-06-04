# python -V 3.8

import sys
import os
import time
import math
import dis
import marshal
import py_compile


class ByteCodeDisassambler:
    """\nusage: usage: bc.py action [-flag value]*
    
    This program compiles file or string into bytecode or yields opcodes (and their arguments) for ordinary python programs from py, pyc and string code:
    
    compile
        -py file.py compile file into bytecode and store it as file.pyc
        -s "src" compile src into bytecode and store it as out.pyc
    print
        -py src.py produce human-readable bytecode from python file
        -pyc src.pyc produce human-readable bytecode from compiled .pyc file
        -s "src" produce human-readable bytecode from normal string
    """

    compiled = False
    src = False

    def __init__(self, arguments=""):
        if len(arguments) > 1 and arguments[0] in ['compile', 'print'] and arguments[1] in ['-py', '-pyc', '-s']:
            if arguments[0] == 'compile':
                if arguments[1] == '-s':
                    self.src = True
                self.__compile_code(arguments[2])
            else:
                if arguments[1] == '-pyc':
                    self.compiled = True
                elif arguments[1] == '-s':
                    self.src = True
                self.__print_result(arguments[2])
        else:
            print(self.__doc__)


    def __compile_code(self, code):
        if self.src:
            with open('out.py', 'w') as f:
                f.write(code)
            py_compile.compile('out.py')
        else:
            py_compile.compile(code)


    def __get_bytecode(self, filename):
        bytecode = False
        if self.src:
            bytecode = dis.Bytecode(filename)
        elif os.path.exists(filename):
            if self.compiled:
                func = open(filename, 'rb')
                code = marshal.load(func)
                bytecode = dis.Bytecode(code)
            else:
                func = open(filename).read()
                bytecode = dis.Bytecode(func)
        return bytecode
        
    # Disable
    def __blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def __enablePrint(self):
        sys.stdout = sys.__stdout__

    def __print_result(self, code):
        if code:
            bc = self.__get_bytecode(code)
            if bc:
                for line in bc:
                    print(line.opname+" "+str(line.argval))
                
       

def main():
    sys_args = sys.argv[1:]
    ByteCodeDisassambler(sys_args)
    

main()