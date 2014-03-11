#!/bin/bash
#PBS -N ScaffDense 
#PBS -l nodes='1':ppn='10'
#PBS -q generic 

dir=/path/to/scaffdense/folder

source ~/.bash_profile

# Run Command Below

cd $dir

module load python/2.7.6
module load augustus/2.7
module load blast

pip install -r scaffdense_requirements.txt --user

python scaffdense.py <scaffold> <blastdb> --threads=10
