"""ScaffDense

Usage:
    scaffdense.py <scaffold> <blastdb> --threads=<threads> [--e-value=<value>] [--n-scaffolds=<top_n_scafs>]

Options:
    <blastdb>                     Nucleotide BLAST database name.
    <scaffold>                    Fasta file with assembled scaffold
    --threads=<threads>           Number of processors to use (int)
    --e-value=<value>             The BLAST e-value for blast results (default: 1e-10)
    --n-scaffolds=<top_n_scafs>   How many of the top n scaffolds to use. Default is top 10 scaffolds.
"""

import os
import operator
import tempfile
import csv
from multiprocessing import Pool, Manager
from docopt import docopt
from Bio import SeqIO
from Bio.Blast import NCBIXML
from plumbum.cmd import perl, grep, augustus, tblastn, rm


TEMPDIR = None
SCAFFOLDS = None
RESULTS = Manager().list()
GENE_COUNTS = dict()

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
        blast_arguments.append(
            {'filename': scaff, 'database': database, 'evalue': evalue})
    pool.map(run_blast, blast_arguments)


def run_fetch_prot_seq(filename):
    pipeline = perl['getAnnoFasta.pl', tmp_path(filename + '.aug')]
    pipeline()

def count_aa_records(filename):
    global GENE_COUNTS
    records = read_fasta(tmp_path(filename + '.aug.aa'))
    GENE_COUNTS[filename] = len(records)

def run_blast(params):
    database = params['database']
    evalue = params['evalue']
    filename = params['filename']
    count_aa_records(filename)
    pipeline = tblastn['-db', database, '-query',
                       tmp_path(filename + '.aug.aa'), '-out',
                       tmp_path(filename + '.xml'),
                       '-outfmt', 5,
                       '-evalue', evalue]
    pipeline()
    count_scaffold_hits(filename)


def count_scaffold_hits(filename):
    global RESULTS, GENE_COUNTS
    scaf_count = dict()
    handle = open(tmp_path(filename + '.xml'), 'r')
    blast_records = list(NCBIXML.parse(handle))
    handle.close()
    for record in blast_records:
        try:
            desc = record.descriptions[0]
            scaffold = str(desc).split(" ")[1]
            if scaffold not in scaf_count:
                scaf_count[scaffold] = 1
            else:
                scaf_count[scaffold] += 1
        except IndexError:
            pass
    total_hits = GENE_COUNTS[filename]
    best_hit_scaf_key = max(scaf_count, key=scaf_count.get)
    best_hit_scaf_count = scaf_count[best_hit_scaf_key]
    RESULTS.append((filename, best_hit_scaf_key, best_hit_scaf_count,
                   total_hits, float(best_hit_scaf_count) / float(total_hits)))


def write_results_csv(filename):
    global RESULTS
    with open(filename + '.csv', 'w') as out:
        file_writer = csv.writer(out)
        file_writer.writerow(
            ['scaffold', 'best_hit_scaffold', 'best_hit_scaffold_count', 'total_hits', 'p'])
        for fields in RESULTS:
            file_writer.writerow([f for f in fields])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.0')

    if arguments['<scaffold>'] and arguments['<blastdb>']:
        filename = get_filename(arguments['<scaffold>'])
        threads = int(arguments['--threads'])
        database = arguments['<blastdb>']
        evalue = arguments['--e-value']
        n_scafs = arguments['--n-scaffolds']
        convert_single_line(filename)
        if n_scafs is None:
            get_top_n_scaffs(filename)
        else:
            get_top_n_scaffs(filename, n=int(n_scafs))
        if evalue is None:
            run_parallel(threads, database)
        else:
            run_parallel(threads, database, evalue=evalue)
        write_results_csv(arguments['<scaffold>'])
        del_tmp()
