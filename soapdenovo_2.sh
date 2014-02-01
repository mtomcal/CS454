#!/bin/bash
#PBS -N name
#PBS -o /home4/mtomcal/logs
#PBS -e /home4/mtomcal/logs
#PBS -d /home4/mtomcal/logs
#PBS -m ae
#PBS -M mtomcal@uoregon.edu
#PBS -l nodes='1':ppn='12'
#PBS -q fatnodes

dir=/home4/mtomcal
out=$dir/output
tmp=/tmp/mtomcal

source $dir/.bash_profile

# Make output folder
mkdir -p $out

# Make tmp folder
mkdir -p $tmp

# Run Command Below
SOAPdenovo-127mer all -s /home14/mstreis/in/soap/config/soap_config_A_2.txt -K 45 -R -F -N 300000000 -o /tmp/mtomcal 1>A_k33_2.log 2>A_k33_2.err.log

# copy data from scratch (or tmp) directory back to home directory for long term storage:
/bin/cp -a $tmp/* $out

# clean up after ourselves so others can utilize scratch:
/bin/rm -rf $tmp


