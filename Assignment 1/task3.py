import os
import subprocess
import datetime
import logging


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
    original_path = os.getcwd()

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
                process, error = run_command(command)
                write_command_log(original_path, process)
        except EOFError:
            print_quit()
            keep_looping = False
        except:
            pass


def run_command(command):
    command_list = command.split(" ")
    process = subprocess.Popen(command_list, shell=True)
    output, error = process.communicate()
    process.wait()

    return process, error


def write_command_log(path, process):
    time_str = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
    cmd_str = process.args[0]
    args_str = process.args[1:]
    pid_str = str(process.pid)
    exit_str = str(process.returncode)
    stdout_str = "stdout"

    log_str = "\n" + time_str + " cmd: " + cmd_str + ", args: " + str(
        args_str) + ", stdout: " + stdout_str + ", pid: " + pid_str + ", exit: " + exit_str

    file_path = path + "/myshell.log"
    f = open(file_path, "a+")
    f.write(log_str)
    f.close()


main()
