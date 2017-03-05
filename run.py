#!/usr/bin/python
import sys
import os
import subprocess
import argparse
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
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if not os.path.isfile(configName):
    sys.stderr.write('Config file %s does not exist' % configName)
    exit(1)

startupIniName = 'startup.ini'
sourceIni = open(configName)  # open ini
lines = sourceIni.readlines()
sourceIni.close()
if mtEnabled:
    lines = lines[:-3]  # remove intro graphic
    lines.append('DISPLAY = mkwrapper\n')
    lines.append('CYCLE_TIME = 0.100\n')
else:
    lines.append('DISPLAY = axis\n')
    lines.append('CYCLE_TIME = 0.200\n')
startupIni = open(startupIniName, 'w')
startupIni.writelines(lines)  # copy file contents
startupIni.close()

try:
    launcher.check_installation()
    launcher.cleanup_session()

    if robotEnabled:  # consider the special robot case
        launcher.load_bbio_file('paralell_cape2_robot.bbio')
    else:
        launcher.load_bbio_file('paralell_cape2.bbio')

    if mtEnabled:  # load Machinetalk services
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

        if os.path.exists('/dev/video0'):  # automatically start videoserver
            launcher.start_process('videoserver -i video.ini Webcam1')

    launcher.start_process('linuxcnc ' + startupIniName)
    while True:
        launcher.check_processes()
        sleep(1)
except subprocess.CalledProcessError:
    launcher.end_session()
    exit(1)

exit(0)
