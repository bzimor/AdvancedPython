# python -V 3.8

import sys
import os
import time
import math


class WhoIsFaster:
    """\nusage: compare.py [files]\n\nThis program takes N arbitrary .py files and creates a neat table out of their execution time ranking by who-is-faster"""

    arguments = ""

    def __init__(self, arguments=""):
        if arguments:
            self.arguments = arguments
            self.__print_result()


    def __get_execution_time(sefl, filename):
        if os.path.exists(filename):
            start_time = time.time()
            exec(open(filename).read())
            end_time = time.time()
            return end_time - start_time
        
    # Disable
    def __blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def __enablePrint(self):
        sys.stdout = sys.__stdout__

    def __print_result(self):
        files = set(self.arguments)
        files_dict = {}
        if files:
            for f in files:
                self.__blockPrint()
                exe_time = self.__get_execution_time(f)
                files_dict[f] = exe_time
            files_dict = {k: v for k, v in sorted(files_dict.items(), key=lambda item: item[1])}
            self.__enablePrint()
            print("PROGRAM | RANK | TIME ELAPSED")
            n = 1
            for k, v in files_dict.items():
                print(k + "    " + str(n) + "     " + str(v) + "s")
                n += 1
       

def main():
    sys_args = sys.argv[1:]
    if sys_args:
        WhoIsFaster(sys_args)
    else:
        print(WhoIsFaster.__doc__)

main()