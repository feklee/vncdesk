#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GtkVnc

from vncdesk import vnc_server
from sys import argv
from vncdesk.util import exit_on_error, settings

def vnc_initialized(src, window):
    print("Connection initialized")
    window.show_all()
    window.set_size_request(int(settings['desktop']['width']),
                            int(settings['desktop']['height']))
    window.set_resizable(False)

def quit_all(widget = None):
    vnc_server.terminate()
    Gtk.main_quit()

def vnc_disconnected(src):
    print("Disconnected from server")
    quit_all()

def exit_with_usage():
    exit_on_error("Usage: " + argv[0] + " NUMBER")

def read_cmd_line():
    if len(argv) != 2:
        exit_with_usage()

    try:
        return int(argv[1])
    except ValueError:
        exit_with_usage()

def main():
    vnc_server.start(read_cmd_line())

    window = Gtk.Window()
    vnc = GtkVnc.Display()

    window.add(vnc)
    window.connect("destroy", quit_all)
    window.set_title(settings['window']['title'])

    vnc.realize()
    vnc.set_pointer_local(False)

    vnc.set_credential(GtkVnc.DisplayCredential.PASSWORD, vnc_server.password)

    vnc.open_host("localhost", str(vnc_server.port))

    vnc.connect("vnc-initialized", vnc_initialized, window)
    vnc.connect("vnc-disconnected", vnc_disconnected)

    Gtk.main()
