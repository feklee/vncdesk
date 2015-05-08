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
    except Exception as e:
        exit_on_error("Cannot read settings: " + str(e))
