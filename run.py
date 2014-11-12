#!/usr/bin/python

import sys
import os
import subprocess
import importlib
import argparse
from time import *


def rip_environment(path=None, force=False):
    if os.getenv('EMC2_PATH') is not None:    # check if already ripped
        return

    if path is None:
        command = None
        scriptFilePath = os.environ['HOME'] + '/.bashrc'
        if os.path.exists(scriptFilePath):
            with open(scriptFilePath) as f:    # use the bashrc
                content = f.readlines()
                for line in content:
                    if 'rip-environment' in line:
                        line = line.strip()
                        if (line[0] == '.'):
                            command = line

        scriptFilePath = os.environ['HOME'] + '/machinekit/scripts/rip-environment'
        if os.path.exists(scriptFilePath):
            command = '. ' + scriptFilePath

        if (command is None):
            sys.stderr.write('Unable to rip environment\n')
            sys.exit(1)
    else:
        command = '. ' + path + '/scripts/rip-environment'

    process = subprocess.Popen(command + ' && env', stdout=subprocess.PIPE, shell=True)
    for line in process.stdout:
        (key, _, value) = line.partition('=')
        os.environ[key] = value.rstrip()

    sys.path.append(os.environ['PYTHONPATH'])

parser = argparse.ArgumentParser(description='starts TheCoolTool configs')
parser.add_argument('config', nargs=1, help='path to config file')

args = parser.parse_args()

configName = args.config[0]

rip_environment()
launcher = importlib.import_module('machinekit.launcher')

launcher.register_exit_handler()
launcher.set_debug_level(5)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    launcher.check_installation()
    launcher.cleanup_session()
    launcher.load_bbio_file('paralell_cape2.bbio')
    #launcher.install_comp('gantry.comp')
    #launcher.install_comp('led_dim.comp')
    #launcher.install_comp('thermistor_check.comp')
    launcher.start_process("configserver ../Machineface ../Cetus/")
    launcher.start_process('linuxcnc ' + configName)
except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)

while True:
    sleep(1)
    launcher.check_processes()
