#!/usr/bin/python

import sys
import os
import subprocess
import importlib
import argparse
from time import *
from machinekit import launcher

parser = argparse.ArgumentParser(description='starts TheCoolTool configs')
parser.add_argument('-nm', '--no_machinetalk', help='disables Machinetalk', action='store_true')
parser.add_argument('config', nargs=1, help='path to config file')

args = parser.parse_args()

configName = args.config[0]
mtEnabled = not args.no_machinetalk

launcher.register_exit_handler()
#launcher.set_debug_level(5)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    launcher.check_installation()
    launcher.cleanup_session()
    launcher.load_bbio_file('paralell_cape2.bbio')
    if mtEnabled:
        launcher.start_process("configserver ../Machineface ../Cetus/")
    launcher.start_process('linuxcnc ' + configName)
except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)

while True:
    sleep(1)
    launcher.check_processes()
