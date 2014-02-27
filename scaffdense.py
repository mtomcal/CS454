"""ScaffDense

Usage:
    scaffdense.py validate <scaffold> <blastdb> --threads=<threads> [--e-value=<value>] [--pbs]
"""

import os
import operator
import tempfile
from multiprocessing import Pool
from docopt import docopt
from Bio import SeqIO
from plumbum.cmd import perl, grep, augustus, blastp, rm


TEMPDIR = None
SCAFFOLDS = None

def open_tmp(filename, flags):
    global TEMPDIR
    if TEMPDIR is None:
        TEMPDIR = tempfile.mkdtemp()
    return open(os.path.join(TEMPDIR, filename), flags)

def del_tmp():
    global TEMPDIR
    pipeline = rm['-r', TEMPDIR]
    pipeline()

def tmp_path(filename):
    global TEMPDIR
    if TEMPDIR is None:
        TEMPDIR = tempfile.mkdtemp()
    return os.path.join(TEMPDIR, filename)


def read_file(filename):
    with open(filename, 'r') as reader:
        return reader.readlines()
    raise IOError


def read_fasta(filename):
    records = SeqIO.index(filename, 'fasta')
    return records


def get_filename(filename):
    return os.path.basename(filename).split('.')[0]

def convert_single_line(filename):
    pipeline = perl['singleline.pl', filename + '.scafSeq'] |\
        grep['-A1', '>scaffold'] \
        > tmp_path('filtered_' + filename + '.fasta')
    pipeline()


def get_top_n_scaffs(filename, n=10):
    global SCAFFOLDS
    records = read_fasta(tmp_path('filtered_' + filename + '.fasta'))
    SCAFFOLDS = list()
    top_n = list()
    sizes = {}
    sorted_sizes = list()
    for key in records:
        sizes[key] = len(records[key].seq)
    sorted_sizes = sorted(sizes.iteritems(), reverse=True,
                          key=operator.itemgetter(1))
    for i in range(1, n):
        item = records[sorted_sizes[i][0]]
        output_name = 'scaf_' + item.name + '.fasta'
        SCAFFOLDS.append(item.name)
        with open(tmp_path(output_name), 'w') as out:
            SeqIO.write(item, out, 'fasta')

def run_augustus(filename):
    pipeline = augustus['--species=arabidopsis',
                        tmp_path('scaf_' + filename + '.fasta')] > tmp_path(filename + '.aug')
    pipeline()

def gene_find(filename):
    run_augustus(filename)
    run_fetch_prot_seq(filename)

def run_parallel(threads, database, evalue="1e-10"):
    global SCAFFOLDS
    if SCAFFOLDS is None:
        raise NameError('SCAFFOLDS is not initialized by get_top_n_scaffs()')
    pool = Pool(threads)

    pool.map(gene_find, SCAFFOLDS)

    blast_arguments = list()
    for scaff in SCAFFOLDS:
        blast_arguments.append((scaff, database, evalue))
    pool.map(run_blast, blast_arguments)

def run_fetch_prot_seq(filename):
    pipeline = perl['getAnnoFasta.pl', tmp_path(filename + '.aug')]
    pipeline()


def run_blast(filename, database, evalue="1e-10"):
    pipeline = blastp['-db', database, '-query',
                      tmp_path(filename + '.aug.aa'), '-out',
                      tmp_path(filename + '.xml'),
                      '-outfmt', 5,
                      '-evalue', evalue]
    pipeline()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1')

    if arguments['<scaffold>'] and arguments['<blastdb>']:
        filename = get_filename(arguments['<scaffold>'])
        threads = int(arguments['--threads'])
        database = arguments['<blastdb>']
        print tmp_path('file')
        convert_single_line(filename)
        get_top_n_scaffs(filename)
        run_parallel(threads, database)
