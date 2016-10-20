from os import path, environ, kill, system, chdir, access, X_OK, getcwd
import string
import signal
from time import sleep
import uuid
import threading
from shlex import quote
from .util import exit_on_error, settings, read_settings

def set_environ(invocation_dir):
    global _display
    environ["WIDTH"] = settings['desktop']['width']
    environ["HEIGHT"] = settings['desktop']['height']
    environ["GUEST_DISPLAY"] = environ["DISPLAY"]
    environ["DISPLAY"] = _display
    environ["INVOCATION_DIR"] = invocation_dir

def terminate():
    global _xvnc_lock_filename

    if path.isfile(_xvnc_lock_filename):
        pid = int(open(_xvnc_lock_filename, 'r').read())
        print(_xvnc_lock_filename)
        try:
            kill(pid, signal.SIGTERM)
        except Exception as ex:
            print("Couldn't kill xvnc process, trying to delete its lock file...\n")
            try:
                os.remove(_xvnc_lock_filename)
            except OSError as e:
                print("Couldn't even find xvnc lock files. Aborting...")
                exit(-1)
            else:
                print("Xvnc terminated\n")
        else:
            print("Xvnc terminated\n")


def wait_for_xvnc():
    while not path.isfile(_xvnc_lock_filename):
        sleep(0.1)

def font_path():
    try:
        from .font_path import font_path
        return font_path
    except ImportError:
        return None

def str2bool(v):
  return v.strip().lower() in ("yes", "true", "t", "1")

def xvnc_cmd():
    global _display, _number, port

    geometry = settings['desktop']['width'] + "x" + \
               settings['desktop']['height']
    depth = settings['desktop']['depth']
    localhost = str2bool(settings['other']['localhost'])
    port = 5900 + _number
    fp = font_path()
    #"-desktop xfig",
    a = ["Xvnc",
         _display,
         "-geometry " + geometry,
         "-rfbauth " + _password_filename,
         "-rfbport " + str(port),
         "-depth " + depth,
         "-pn"]
    if localhost:
        a.append("-localhost ")
    if fp:
        a.append("-fp " + fp)
    a.append("&")

    return " ".join(a)

def start_xvnc():
    terminate()
    cmd = xvnc_cmd()
    print("CMD: "+cmd)
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

def startup(filename, arguments, invocation_dir):
    set_environ(invocation_dir)
    quoted_arguments = list(map(quote, arguments))
    cmd = filename + " " + " ".join(quoted_arguments)
    system(cmd)
    terminate()
    quit()

def run_startup(arguments, invocation_dir):
    filename = "./startup"
    check_startup(filename)
    t1 = threading.Thread(target = startup, args = [filename,
                                                    arguments,
                                                    invocation_dir])
    t1.start()

def configure_xvnc():
    global _number
    system("vncconfig -display=:" + str(_number) + " -list >/dev/null 2>&1" +
           " && (vncconfig -nowin -display=:" + str(_number) + " &)" +
           " || echo 'vncconfig not available'")

def change_to_configuration_dir():
    global _number
    dirname = path.join(environ["HOME"], ".vncdesk", str(_number))
    try:
        chdir(dirname)
    except:
        exit_on_error("Cannot access directory " + dirname)

def start(number, arguments):
    global _number, _display, _xvnc_lock_filename

    _number = number
    _display = ':' + str(_number)
    _xvnc_lock_filename = "/tmp/.X" + str(_number) + "-lock"

    invocation_dir = getcwd()
    change_to_configuration_dir()
    read_settings()
    create_password()
    start_xvnc()
    configure_xvnc()
    run_startup(arguments, invocation_dir)
