#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkVnc', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GtkVnc

from . import vnc_server
from sys import argv
from os import environ
from .util import exit_on_error, settings
from .version import __version__

def vnc_initialized(src, window):
    print("Connection initialized")
    f = settings['window']['scale_factor']
    window.show_all()
    window.set_size_request(round(f * settings['desktop']['width']),
                            round(f * settings['desktop']['height']))
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

def ensure_display():
    if not "DISPLAY" in environ:
        exit_on_error("DISPLAY not set");
        # if DISPLAY is not set, then - as of December 2016 - the VNC client may
        # segfault

def read_cmd_line():
    if len(argv) < 2:
        exit_with_usage()

    try:
        return (int(argv[1]), argv[2:])
    except ValueError:
        exit_with_usage()

def gtk_vnc_allows_configuring_smoothing(vnc):
    return 'set_smoothing' in dir(vnc)

def main():
    number, arguments = read_cmd_line()

    ensure_display()

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

    if gtk_vnc_allows_configuring_smoothing(vnc):
        vnc.set_smoothing(settings['window']['smoothing'])

    vnc.set_credential(GtkVnc.DisplayCredential.PASSWORD, vnc_server.password)

    vnc.open_host("localhost", str(vnc_server.port))

    vnc.connect("vnc-initialized", vnc_initialized, window)
    vnc.connect("vnc-disconnected", vnc_disconnected)

    Gtk.main()
