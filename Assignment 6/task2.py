# python -V 3.8
import sys
import operator


class ATree:
    def __init__(self, val):
        self.value = val
        self.left_child = None
        self.right_child = None

    def set_val(self, val):
        self.value = val

    def set_left(self, val):
        self.left_child = ATree(val)

    def set_right(self, val):
        self.right_child = ATree(val)


class Cas:
    """
    Please always separate number and operator with space
    Example: 37 + -31, 1 - 20

    Use 'exit' command to close the program
    """

    def __init__(self, arguments=""):
        if len(arguments) > 0 and arguments[0] == '-h':
            print(self.__doc__)
        else:
            self.__saved_result__ = []
            self.__run_cas__()

    def __run_cas__(self):
        keep_looping = True

        while keep_looping:
            try:
                command = input("\n>> ")
                if command == 'exit':
                    keep_looping = False
                elif command != '':
                    tree = self.__parse_input__(command)
                    if tree is not None:
                        result = self.__eval_result__(tree)
                        self.__saved_result__.append(result)
                        print(len(self.__saved_result__), ':', result)
            except EOFError:
                keep_looping = False

    def __parse_input__(self, command):
        tokens = command.split(' ')
        tokens.reverse()
        p_stack = []
        parse_tree = ATree('')
        p_stack.append(parse_tree)
        current_node = parse_tree

        first_time = True
        for index, val in enumerate(tokens):
            if val == '(':
                current_node.set_left('')
                p_stack.append(current_node)
                current_node = current_node.left_child
            elif val in ['+', '-']:
                current_node.set_val(val)
                current_node.set_right('')
                current_node = current_node.right_child
            elif val == ')':
                current_node = p_stack.pop()
            elif val not in ['+', '-', ')']:
                try:
                    if first_time:
                        current_node.set_left(int(val))
                        first_time = False
                        parent = p_stack.pop()
                        current_node = parent
                    else:
                        if index == len(tokens)-1:
                            current_node.set_val(int(val))
                        else:
                            current_node.set_left(int(val))
                except ValueError:
                    print('err: invalid number')
                    return None

        return parse_tree

    def __eval_result__(self, tree):
        op = {'+': operator.add, '-': operator.sub}

        left_child = tree.left_child
        right_child = tree.right_child

        if left_child is not None and right_child is not None:
            fn = op[tree.value]
            return fn(self.__eval_result__(right_child), self.__eval_result__(left_child))
        else:
            return tree.value


def main():
    sys_args = sys.argv[1:]
    Cas(sys_args)


main()
