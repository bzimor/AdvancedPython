# python -V 3.8

import sys
import os
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
    compare -format src [-format src]+
         produce bytecode comparison for giving sources
         (supported formats -py, -pyc, -s)
    """

    compiled = False
    src = False

    def __init__(self, arguments=""):
        if len(arguments) > 1 and arguments[0] in ['compile', 'print', 'compare'] and arguments[1] in ['-py', '-pyc', '-s']:
            if arguments[0] == 'compile':
                if arguments[1] == '-s':
                    self.src = True
                self.__compile_code(arguments[2])
            elif arguments[0] == 'print':
                if arguments[1] == '-pyc':
                    is_compiled = True
                elif arguments[1] == '-s':
                    is_src = True
                self.__print_result(arguments[2], is_src, is_compiled)
            else:
                file_arguments = arguments[1:]
                if (len(file_arguments) % 2) == 0:
                    self.__compare(file_arguments)
                else:
                    print('Arguments missmatch')
        else:
            print(self.__doc__)

    def __compile_code(self, code):
        if self.src:
            with open('out.py', 'w') as f:
                f.write(code)
            py_compile.compile('out.py')
        else:
            py_compile.compile(code)

    def __get_bytecode(self, filename, is_src, is_compiled):
        bytecode = False
        if is_src:
            bytecode = dis.Bytecode(filename)
        elif os.path.exists(filename):
            header_size = 8
            if sys.version_info >= (3, 6):
                header_size = 12
            if sys.version_info >= (3, 7):
                header_size = 16
            if is_compiled:
                with open(filename, "rb") as fh:
                    # ignore header
                    header_bytes = fh.read(header_size)
                    code = marshal.load(fh)
                    bytecode = dis.Bytecode(code)
            else:
                func = open(filename).read()
                bytecode = dis.Bytecode(func)
        return bytecode

    def __compare(self, arguments):
        files_dict = dict()
        n = len(arguments)
        for i in range(1, n, 2):
            if arguments[i - 1] in ['-s', '-pyc', '-py']:
                file_name = arguments[i]
                file_type = arguments[i - 1]
                files_dict[file_name] = file_type
            else:
                pass

        if len(files_dict) > 0:
            raw_result = self.__compare_bytecode(files_dict)
            # sorting the result
            sorted_result = sorted(raw_result.items(), key=lambda x: max(x[1]), reverse=True)

            # make header string
            header_str = "{:13}".format('Instruction')
            for x in files_dict.keys():
                header_str += "|{:13}".format(x[:13])

            # make body string from sorted result
            body_str = ''
            for x in sorted_result:
                body_str += "{:13}".format(x[0][:13])
                for i in range(0, len(files_dict)):
                    body_str += "|{:<13}".format(x[1][i])
                body_str += "\n"

            # print formatted string
            print(header_str)
            print(body_str)
        else:
            pass

    def __compare_bytecode(self, arguments):
        compared_result = dict()
        i = 0
        for key, value in arguments.items():
            file_type = value
            # Checking parameter, it it is -s or -pyc or -py
            is_src = False
            is_compiled = False
            if file_type == '-s':
                is_src = True
            elif file_type == '-pyc':
                is_compiled = True

            bytecode = self.__get_bytecode(key, is_src, is_compiled)
            for line in bytecode:
                if line.opname not in compared_result:
                    # make empty array which is equals to argument length (number of file or source)
                    compared_result[line.opname] = [0] * len(arguments)
                compared_result[line.opname][i] += 1
            i += 1

        # return dictionary in format { OPNAME : [n array], ... }
        return compared_result

    # Disable
    def __blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def __enablePrint(self):
        sys.stdout = sys.__stdout__

    def __print_result(self, code, is_src, is_compiled):
        if code:
            bc = self.__get_bytecode(code, is_src, is_compiled)
            if bc:
                for line in bc:
                    print(line.opname + " " + str(line.argval))


def main():
    sys_args = sys.argv[1:]
    ByteCodeDisassambler(sys_args)


main()
