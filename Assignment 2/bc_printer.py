# python -V 3.8

import sys
import os
import time
import math
import dis


class ByteCodeDisassambler:
    """\nusage: bc_printer.py -py src.py\n\nThis program yields opcodes (and their arguments) for ordinary python programs"""

    argument = ""

    def __init__(self, arguments=""):
        if len(arguments) > 1 and arguments[0] == '-py':
            self.argument = arguments[1]
            print(arguments[1])
            self.__print_result()
        else:
            print(self.__doc__)


    def __get_bytecode(self, filename):
        if os.path.exists(filename):
            func = open(filename).read()
            bytecode = dis.Bytecode(func)
            return bytecode
        
    # Disable
    def __blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def __enablePrint(self):
        sys.stdout = sys.__stdout__

    def __print_result(self):
        if self.argument:
            bf = self.__get_bytecode(self.argument)
            for line in bf:
                print(line.opname+" "+str(line.argval))
                
       

def main():
    sys_args = sys.argv[1:]
    ByteCodeDisassambler(sys_args)
    

main()