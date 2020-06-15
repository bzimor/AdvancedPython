import os

def main():
    '''
    Main function of the shell
    '''
    do_exit = False
    while not do_exit:
        # get absolute current path,
        # then truncate every folder to 1 char (2 if starts with a ".")
        path = os.path.abspath(os.getcwd())
        path = "/".join([i[0] if i[0] != "." else i[0] + i[1] for i in path.split("/") if len(i) > 0])