# Python 3.7.5
import os


def print_quit():
    print("\nGoodbye!\n# Now we’re back in normal shell")


def change_dir(target_path):
    try:
        os.chdir(target_path)
    except FileNotFoundError:
        print(target_path + ' does NOT exist.')


def get_current_path(current_path):
    try:
        path_str = "".join("/" + (x[0] if x[0] != "." else x[0:2]) for x in current_path[1:].split("/"))
        return path_str
    except:
        return ""


def run_command(command):
    os.system(command)


def main():
    keep_looping = True
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    while keep_looping:
        current_path = os.getcwd()
        current_path_str = get_current_path(current_path)

        command_str = "\nmyshell [" + current_path_str + "]:"
        try:
            command = input(command_str)
            if command == 'exit':
                print_quit()
                keep_looping = False
            elif command[0:2] == "cd":
                split_command = command.split(" ")
                if len(split_command) > 1:
                    target_path = command.split(" ")[1]
                    change_dir(target_path)
            else:
                run_command(command)
        except EOFError:
            print_quit()
            keep_looping = False
        except:
            print("Error!")


main()
