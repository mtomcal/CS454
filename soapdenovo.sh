#!/bin/bash -l
#PBS -N A_k45_2
#PBS -o /home4/mtomcal/logs
#PBS -e /home4/mtomcal/logs
#PBS -d /home4/mtomcal/logs
#PBS -l nodes='1':ppn='12'
#PBS -q fatnodes

# Load any modules needed to run your software
module load soapdenovo/2.04

# execute program here:
SOAPdenovo-127mer all -s /home14/mstreis/in/soap/config/soap_config_A_2.txt -K 45 -R -F -N 300000000 -o /tmp/mtomcal 1>A_k33_2.log 2>A_k33_2.err.log
# copy data from scratch (or tmp) directory back to home directory for long term storage:
mkdir -p /home4/mtomcal/CS454/out/k45
/bin/cp -a /tmp/mtomcal/* /home4/mtomcal/CS454/out/k45

# clean up after ourselves so others can utilize scratch:
/bin/rm -rf /tmp/mtomcal


