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
$dir/abyss-1.3.7/bin/abyss-pe k=64 name=flower lib='pe1' mp='mp1 mp2 mp3' \
pe1='/home14/mstreis/in/PE_A/PE_fil_R1.fastq /home14/mstreis/in/PE_A/PE_fil_R2.fastq' 
mp1='/home14/mstreis/in/mate_pair-112613/prc_sr_out_ACAGTG/ACAGTG_R1.fastq /home14/mstreis/in/mate_pair-112613/prc_sr_out_ACAGTG/ACAGTG_R2.fastq' \
mp2='/home14/mstreis/in/mate_pair-112613/prc_sr_out_GCCAAT/GCCAAT_R1.fastq /home14/mstreis/in/mate_pair-112613/prc_sr_out_GCCAAT/GCCAAT_R2.fastq' \
mp3='/home14/mstreis/in/mate_pair-112613/prc_sr_out_ATGTCA/ATGTCA_R1.fastq /home14/mstreis/in/mate_pair-112613/prc_sr_out_ATGTCA/ATGTCA_R2.fastq'

# copy data from scratch (or tmp) directory back to home directory for long term storage:
/bin/cp -a $tmp/* $out

# clean up after ourselves so others can utilize scratch:
/bin/rm -rf $tmp


