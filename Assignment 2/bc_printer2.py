# python -V 3.8

import sys
import os
import dis
import marshal


class ByteCodeDisassambler:
    """\nusage: bc_printer.py -format src
    
    This program yields opcodes (and their arguments) for ordinary python programs from py, pyc and string code:
    
    -py src.py produce human-readable bytecode from python file
    
    -pyc src.pyc produce human-readable bytecode from compiled .pyc file
    
    -s "src" produce human-readable bytecode from normal string

    """

    argument = ""
    compiled = False
    src = False

    def __init__(self, arguments=""):
        if len(arguments) > 1 and arguments[0] in ['-py', '-pyc', '-s']:
            if arguments[0] == '-pyc':
                self.compiled = True
            elif arguments[0] == '-s':
                self.src = True
            self.argument = arguments[1]
            self.__print_result()
        else:
            print(self.__doc__)


    def __get_bytecode(self, filename):
        bytecode = False
        if self.src:
            bytecode = dis.Bytecode(filename)
        elif os.path.exists(filename):
            if self.compiled:
                header_size = 8
                if sys.version_info >= (3, 6):
                    header_size = 12
                if sys.version_info >= (3, 7):
                    header_size = 16
                if self.compiled:
                    with open(filename, "rb") as fh:
                        # ignore header
                        header_bytes = fh.read(header_size)
                        code = marshal.load(fh)
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

    def __print_result(self):
        if self.argument:
            bc = self.__get_bytecode(self.argument)
            if bc:
                for line in bc:
                    print(line.opname+" "+str(line.argval))
                
       

def main():
    sys_args = sys.argv[1:]
    ByteCodeDisassambler(sys_args)
    

main()