from os import path, environ, kill, chdir, access, X_OK, getcwd, urandom
import string
import signal
from time import sleep
import uuid
import threading
from sys import exit
from shlex import quote
from .util import exit_on_error, settings, read_settings, log_and_call
from .util import silently_remove, touch
import socket
import subprocess
import binascii
from . import d3des

def set_environ(invocation_dir, xauthority_path):
    global _display
    environ["WIDTH"] = str(settings['desktop']['width'])
    environ["HEIGHT"] = str(settings['desktop']['height'])
    environ["GUEST_DISPLAY"] = environ["DISPLAY"]
    environ["DISPLAY"] = _display
    environ["INVOCATION_DIR"] = invocation_dir
    environ["XAUTHORITY"] = xauthority_path

def remove_lock_file():
    try:
        silently_remove(_xvnc_lock_filename)
    except:
        exit("Cannot remove lock file " + _xvnc_lock_filename)

def terminate():
    global _xvnc_lock_filename

    if path.isfile(_xvnc_lock_filename):
        pid = int(open(_xvnc_lock_filename, 'r').read())
        try:
            kill(pid, signal.SIGTERM)
        except:
            remove_lock_file()

def wait_for_xvnc():
    while not path.isfile(_xvnc_lock_filename):
        sleep(0.1)

def font_path():
    try:
        from .font_path import font_path
        return font_path
    except ImportError:
        return None

def xvnc_cmd(xauthority_path):
    global _display, _number, port

    geometry = str(settings['desktop']['width']) + "x" + \
               str(settings['desktop']['height'])
    depth = str(settings['desktop']['depth'])
    port = 5900 + _number
    fp = font_path()
    a = ["Xvnc",
         _display,
         "-geometry " + geometry,
         "-rfbauth " + _password_filename,
         "-rfbport " + str(port),
         "-depth " + depth,
         "-pn",
         "-localhost",
         "-auth " + xauthority_path]
    if fp:
        a.append("-fp " + fp)
    a.append("&")

    return " ".join(a)

def start_xvnc(xauthority_path):
    terminate()
    log_and_call(xvnc_cmd(xauthority_path))
    wait_for_xvnc()

# see: http://www.geekademy.com/2010/10/creating-hashed-password-for-vnc.html
def vnc_encode(password):
    passpadd = (password + '\x00'*8)[:8]
    strkey = ''.join([ chr(x) for x in d3des.vnckey ])
    ekey = d3des.deskey(bytearray(strkey, encoding="ascii"), False)
    return d3des.desfunc(bytearray(passpadd, encoding="ascii"), ekey)

def write_password_to_file():
    global _password_filename
    _password_filename = ".passwd"
    try:
        password_file = open(_password_filename, "wb")
        password_file.write(vnc_encode(password))
    except:
        exit_on_error("Cannot write to " + _password_filename)

def create_password():
    global password
    password = str(uuid.uuid4())
    write_password_to_file()

def mcookie():
    return binascii.hexlify(urandom(16)).decode()

def add_cookie(xauthority_path, host, cookie):
    global _number
    subprocess.call("xauth -f " + xauthority_path + " add " + host + ":" +
                    str(_number) + " . " + cookie, shell = True)

def create_xauthority(configuration_dir):
    xauthority_path = path.join(configuration_dir, ".Xauthority")
    host = socket.gethostname()
    cookie = mcookie()

    try:
        silently_remove(xauthority_path)
        touch(xauthority_path)
    except:
        exit_on_error("Cannot recreate " + xauthority_path)

    add_cookie(xauthority_path, host, cookie)
    add_cookie(xauthority_path, host + "/unix", cookie)

    return xauthority_path

def check_startup(filename):
    if not path.isfile(filename) or not access(filename, X_OK):
        exit_on_error("Cannot find executable startup script")

def startup(filename, arguments, invocation_dir, xauthority_path):
    set_environ(invocation_dir, xauthority_path)
    quoted_arguments = list(map(quote, arguments))
    log_and_call(filename + " " + " ".join(quoted_arguments))
    terminate()
    quit()

def run_startup(arguments, invocation_dir, xauthority_path):
    filename = "./startup"
    check_startup(filename)
    t1 = threading.Thread(target = startup, args = [filename,
                                                    arguments,
                                                    invocation_dir,
                                                    xauthority_path])
    t1.start()

def configure_xvnc(xauthority_path):
    global _number
    log_and_call("export XAUTHORITY=" + xauthority_path +
                 "; vncconfig -display=:" + str(_number) +
                 " -list >/dev/null 2>&1" +
                 " && (vncconfig -nowin -display=:" + str(_number) + " &)" +
                 " || echo 'Failure running vncconfig'")

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
    configuration_dir = getcwd()
    read_settings()
    create_password()
    xauthority_path = create_xauthority(configuration_dir)
    start_xvnc(xauthority_path)
    configure_xvnc(xauthority_path)
    run_startup(arguments, invocation_dir, xauthority_path)
