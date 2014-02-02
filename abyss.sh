#!/bin/bash
#PBS -N abyss
#PBS -o /home14/wyu/abyss
#PBS -e /home14/wyu/abyss
#PBS -d /home14/wyu/abyss
#PBS -m ae
#PBS -M wyu@uoregon.edu
#PBS -l nodes='1':ppn='12'
#PBS -q fatnodes

dir=/home14/wyu
out=$dir/abyss/output
tmp=/tmp/wyu

source $dir/.bash_profile

# Make output folder
mkdir -p $out

# Make tmp folder
mkdir -p $tmp
module load mpi-tor/openmpi-1.5.4_gcc-4.5.3

# Run Command Below
$dir/abyss-1.3.7/bin/abyss-pe -C $tmp \
k=64 name=flower lib='pe1' mp='mp1 mp2 mp3' \
pe1='/home14/mstreis/in/PE_A/PE_fil_R1.fastq /home14/mstreis/in/PE_A/PE_fil_R2.fastq' 
mp1='/home14/mstreis/in/mate_pair-112613/prc_sr_out_ACAGTG/ACAGTG_R1.fastq /home14/mstreis/in/mate_pair-112613/prc_sr_out_ACAGTG/ACAGTG_R2.fastq' \
mp2='/home14/mstreis/in/mate_pair-112613/prc_sr_out_GCCAAT/GCCAAT_R1.fastq /home14/mstreis/in/mate_pair-112613/prc_sr_out_GCCAAT/GCCAAT_R2.fastq' \
mp3='/home14/mstreis/in/mate_pair-112613/prc_sr_out_ATGTCA/ATGTCA_R1.fastq /home14/mstreis/in/mate_pair-112613/prc_sr_out_ATGTCA/ATGTCA_R2.fastq' \


# copy data from scratch (or tmp) directory back to home directory for long term storage:
/bin/cp -a $tmp/* $out

# clean up after ourselves so others can utilize scratch:
/bin/rm -rf $tmp


