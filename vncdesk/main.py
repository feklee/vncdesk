#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GtkVnc

from . import vnc_server
from sys import argv
from .util import exit_on_error, settings
from .version import __version__

def vnc_initialized(src, window):
    print("Connection initialized")
    f = float(settings['window']['scale_factor'])
    window.show_all()
    print(f * int(settings['desktop']['width']))
    window.set_size_request(round(f * int(settings['desktop']['width'])),
                            round(f * int(settings['desktop']['height'])))
    window.set_resizable(False)

def quit_all(widget = None):
    vnc_server.terminate()
    Gtk.main_quit()

def vnc_disconnected(src):
    print("Disconnected from server")
    quit_all()

def exit_with_usage():
    url = "https://github.com/feklee/vncdesk/tree/v" + __version__
    exit_on_error("""\
Usage: %s NUMBER [ARGUMENT]...
Version: %s
Documentation: <%s>""" % (argv[0], __version__, url))

def read_cmd_line():
    if len(argv) < 2:
        exit_with_usage()

    try:
        return (int(argv[1]), argv[2:])
    except ValueError:
        exit_with_usage()

def main():
    number, arguments = read_cmd_line()
    vnc_server.start(number, arguments)

    window = Gtk.Window()
    vnc = GtkVnc.Display()

    window.add(vnc)
    window.connect("destroy", quit_all)
    window.set_title(settings['window']['title'])
    window.set_wmclass(settings['window']['name'], settings['window']['class'])

    vnc.realize()
    vnc.set_scaling(True)
    vnc.set_pointer_local(False)

    vnc.set_credential(GtkVnc.DisplayCredential.PASSWORD, vnc_server.password)

    vnc.open_host("localhost", str(vnc_server.port))

    vnc.connect("vnc-initialized", vnc_initialized, window)
    vnc.connect("vnc-disconnected", vnc_disconnected)

    Gtk.main()
