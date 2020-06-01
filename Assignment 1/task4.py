import os
import subprocess
import datetime


def print_quit():
    print("\nGoodbye!\n# Now we’re back in normal shell")


def change_dir(target_path):
    try:
        os.chdir(target_path)
    except FileNotFoundError:
        pass


def get_current_path(current_path):
    try:
        path_str = "".join("/" + (x[0] if x[0] != "." else x[0:2]) for x in current_path[1:].split("/"))
        return path_str
    except:
        return ""


def main():
    keep_looping = True
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    original_path = os.getcwd()

    # funny infinite loop
    while keep_looping:
        current_path = os.getcwd()
        current_path_str = get_current_path(current_path)

        command_str = "\nmyshell [" + current_path_str + "]:"
        try:
            command = input(command_str)
            if command == 'exit':
                print_quit()
                keep_looping = False
            else:
                process, error, output = run_command(command)
                write_command_log(original_path, command, process, output)

                if process.returncode != 0:
                    write_error_log(original_path, error)
        except EOFError:
            print_quit()
            keep_looping = False
        except:
            pass


def run_command(command):
    # Q: if we use subprocess.PIPE we can hide the error but we can't run in the interactive mode like 'python' command
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, close_fds=True, text=True)
    output = process.stdout.read()
    print(output.strip())
    error = process.communicate()[1]

    if command[0:2] == "cd":
        # Q: can't use subprocess directly, the error should be handle separately
        split_command = command.split(" ")
        if len(split_command) > 1:
            target_path = command.split(" ")[1]
            change_dir(target_path)

    return process, str(error), output


# Q: command log is still manual
def write_command_log(path, command, process, output):
    command_list = command.split(" ")
    time_str = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
    cmd_str = command_list[0]
    args_str = command_list[1:]
    pid_str = str(process.pid)
    exit_str = str(process.returncode)
    stdout_str = str(len(output.split("\n")))

    log_str = "\n" + time_str + " cmd: " + cmd_str + ", args: " + str(
        args_str) + ", stdout: " + stdout_str + ", pid: " + pid_str + ", exit: " + exit_str

    file_path = path + "/myshell.log"
    f = open(file_path, "a+")
    f.write(log_str)
    f.close()


def write_error_log(path, log):
    file_path = path + "/myshell.stderr"
    f = open(file_path, "a+")
    f.write(log.strip() + "\n")
    f.close()


main()
