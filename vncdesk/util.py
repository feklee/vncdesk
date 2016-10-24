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
        for k, v in new_settings.items():
            settings[k] = v
        if 'window' not in settings:
            settings['window'] = {}
        if 'other' not in settings:
            settings['other'] = {}
        if 'title' not in settings['window']:
            settings['window']['title'] = 'Vncdesk'
        if 'name' not in settings['window']:
            settings['window']['name'] = 'vncdesk'
        if 'class' not in settings['window']:
            settings['window']['class'] = 'Vncdesk'
        if 'scale_factor' not in settings['window']:
            settings['window']['scale_factor'] = '1'
        if 'depth' not in settings['desktop']:
            settings['desktop']['depth'] = '16'
    except Exception as e:
        exit_on_error("Cannot read settings: " + str(e))
