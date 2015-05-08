from os import path, environ, kill, system, chdir, access, X_OK
import string
import signal
from time import sleep
import uuid
import threading
from .util import exit_on_error, settings, read_settings

def set_environ():
    global _display
    environ["WIDTH"] = settings['desktop']['width']
    environ["HEIGHT"] = settings['desktop']['height']
    environ["GUEST_DISPLAY"] = environ["DISPLAY"]
    environ["DISPLAY"] = _display

def terminate():
    global _xvnc_lock_filename

    if path.isfile(_xvnc_lock_filename):
        pid = int(open(_xvnc_lock_filename, 'r').read())
        kill(pid, signal.SIGTERM)

def wait_for_xvnc():
    while not path.isfile(_xvnc_lock_filename):
        sleep(0.1)

def start_xvnc():
    global _display, _number, port

    geometry = settings['desktop']['width'] + "x" + \
               settings['desktop']['height']
    port = 5900 + _number
    cmd = " ".join(["Xvnc",
                    _display,
                    "-desktop xfig",
                    "-geometry " + geometry,
                    "-rfbauth " + _password_filename,
                    "-rfbport " + str(port),
                    "-pn",
                    "&"])
    terminate()
    system(cmd)
    wait_for_xvnc()

def write_password_to_file():
    global _password_filename
    _password_filename = ".passwd"
    cmd = ";".join([
        "rm -f " + _password_filename,
        "umask 177",
        "|".join([
            "echo '" + password + "'",
            "vncpasswd -f >" + _password_filename
        ])
    ])
    system(cmd)

def create_password():
    global password
    password = str(uuid.uuid4())
    write_password_to_file()

def check_startup(filename):
    if not path.isfile(filename) or not access(filename, X_OK):
        exit_on_error("Cannot find executable startup script")

def startup(filename):
    set_environ()
    check_startup(filename)
    system(filename)
    terminate()
    quit()

def run_startup():
    filename = "./startup"
    check_startup(filename)
    t1 = threading.Thread(target = startup, args=(filename,))
    t1.start()

def configure_xvnc():
    global _number
    system("vncconfig -nowin -display=:" + str(_number) + " &")

def change_to_configuration_dir():
    global _number
    dirname = path.join(environ["HOME"], ".vncdesk", str(_number))
    try:
        chdir(dirname)
    except:
        exit_on_error("Cannot access directory " + dirname)

def start(number):
    global _number, _display, _xvnc_lock_filename

    _number = number
    _display = ':' + str(_number)
    _xvnc_lock_filename = "/tmp/.X" + str(_number) + "-lock"

    change_to_configuration_dir()
    read_settings()
    create_password()
    start_xvnc()
    configure_xvnc()
    run_startup()
