import os


def print_quit():
    print("\nGoodbye!\n# Now we’re back in normal shell")


def main():
    keep_looping = True
    while keep_looping:
        try:
            command = input("\nmyshell: ")
            if command == 'exit':
                print_quit()
                keep_looping = False
            else:
                os.system(command)
        except EOFError:
            print_quit()
            keep_looping = False


main()