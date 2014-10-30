#!/bin/bash
config-pin -f paralell_cape2.bbio
configserver
linuxcnc $1
