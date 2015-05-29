#!/usr/bin/python
import sys
import os
import subprocess
import argparse
import tempfile
import shutil
from time import sleep
from machinekit import launcher

if sys.version_info >= (3, 0):
    import configparser
else:
    import ConfigParser as configparser


parser = argparse.ArgumentParser(description='starts TheCoolTool configs')
parser.add_argument('-nm', '--no_machinetalk', help='legacy option', action='store_true')
parser.add_argument('-mk', '--mkwrapper', help='enables mkwrapper mode', action='store_true')
parser.add_argument('-m', '--machineface', help='displays the Machineface user interface', action='store_true')
parser.add_argument('-c', '--cetus', help='displays the Cetus user interface', action='store_true')
parser.add_argument('-r', '--robot', help='enables robot interaction', action='store_true')
parser.add_argument('config', nargs=1, help='path to config file')

args = parser.parse_args()

configName = args.config[0]
mtEnabled = args.mkwrapper
robotEnabled = args.robot
machineface = args.machineface
cetus = args.cetus

launcher.register_exit_handler()
#launcher.set_debug_level(5)
if mtEnabled:
    launcher.set_machinekit_ini('machinekit.ini')
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if not os.path.isfile(configName):
    sys.stderr.write('Config file %s does not exist' % configName)
    exit(1)

startupIniName = 'startup.ini'
sourceIni = open(configName)  # open ini
startupIni = open(startupIniName, 'w')
startupIni.write(sourceIni.read())  # copy file contents
if mtEnabled:
    startupIni.write('DISPLAY = mkwrapper\n')
else:
    startupIni.write('DISPLAY = axis\n')
startupIni.close()
sourceIni.close()

try:
    launcher.check_installation()
    launcher.cleanup_session()
    if robotEnabled:
        launcher.load_bbio_file('paralell_cape2_robot.bbio')
    else:
        launcher.load_bbio_file('paralell_cape2.bbio')
    if mtEnabled:
        cfg = configparser.ConfigParser({'NAME': ''})
        cfg.read(startupIniName)
        machineName = cfg.get('EMC', 'NAME')

        command = 'configserver'
        if machineName is not '':
            command += ' -n %s' % machineName
        if machineface:
            command += ' ~/Machineface'
        if cetus:
            command += ' ~/Cetus'
        launcher.start_process(command)
    launcher.start_process('linuxcnc ' + startupIniName)
    while True:
        launcher.check_processes()
        sleep(1)
except subprocess.CalledProcessError:
    launcher.end_session()
    exit(1)

exit(0)
