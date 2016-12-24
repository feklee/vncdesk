from sys import exit, stderr
import configparser
from copy import deepcopy

settings = {}

def exit_on_error(msg):
    stderr.write(msg + "\n")
    exit(1)

def read_settings():
    try:
        new_settings = configparser.ConfigParser()
        new_settings.read('settings.ini')

        settings['desktop'] = {}
        settings['desktop']['width'] = new_settings.getint('desktop', 'width')
        settings['desktop']['height'] = new_settings.getint('desktop',
                                                            'height')
        settings['desktop']['depth'] = (
            new_settings.getint('desktop', 'depth')
            if new_settings.has_option('desktop', 'depth')
            else 16
        )

        settings['window'] = {}
        settings['window']['title'] = (
            new_settings.get('window', 'title')
            if new_settings.has_option('window', 'title')
            else 'Vncdesk'
        )
        settings['window']['name'] = (
            new_settings.get('window', 'name')
            if new_settings.has_option('window', 'name')
            else 'vncdesk'
        )
        settings['window']['class'] = (
            new_settings.get('window', 'class')
            if new_settings.has_option('window', 'class')
            else 'Vncdesk'
        )
        settings['window']['scale_factor'] = (
            new_settings.getfloat('window', 'scale_factor')
            if new_settings.has_option('window', 'scale_factor')
            else 1
        )
        settings['window']['smoothing'] = (
            new_settings.getboolean('window', 'smoothing')
            if new_settings.has_option('window', 'smoothing')
            else True
        )
    except Exception as e:
        exit_on_error("Cannot read settings: " + str(e))
