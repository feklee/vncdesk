from sys import exit, stderr

def exit_on_error(msg):
    stderr.write(msg + "\n")
    exit(1)
