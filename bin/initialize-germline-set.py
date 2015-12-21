#!/usr/bin/env python
import os
import argparse
import csv
import shutil
import glob
import sys
sys.path.insert(1, './python')
from Bio import SeqIO
from subprocess import check_call

import utils

# ----------------------------------------------------------------------------------------
def clean_dir():
    if os.path.exists(args.dirname):
        for fname in files_to_copy + [unaligned_fname, aligned_fname]:
            if os.path.exists(args.dirname + '/' + fname):
                os.remove(args.dirname + '/' + fname)
        remaining_files = glob.glob(args.dirname + '/*')
        if len(remaining_files) > 0:
            raise Exception('unexpected files in %s: %s' % (args.dirname, ' '.join(remaining_files)))
    else:
        os.makedirs(args.dirname)

# ----------------------------------------------------------------------------------------
def align_new_genes(old_aligned_genes, genes_without_alignments, all_new_genes):
    print 'missing alignments for %d genes' % len(genes_without_alignments)
    old_aligned_fname = args.dirname + '/old-aligned.fasta'
    missing_fname = args.dirname + '/missing-alignments.fasta'
    msa_table_fname = args.dirname + '/msa-table.txt'
    all_fname = args.dirname + '/all.fa'
    with open(old_aligned_fname, 'w') as tmpfile:
        for gene, seq in old_aligned_genes.items():
            tmpfile.write('>%s\n%s\n' % (gene, seq.replace('.', '-')))
    with open(missing_fname, 'w') as tmpfile:
        for gene, seq in genes_without_alignments.items():
            tmpfile.write('>%s\n%s\n' % (gene, seq.replace('.', '-')))
    check_call('ruby bin/makemergetable.rb ' + old_aligned_fname + ' 1>' + msa_table_fname, shell=True)
    check_call('cat ' + old_aligned_fname + ' ' + missing_fname + ' >' + all_fname, shell=True)
    check_call('mafft --merge ' + msa_table_fname + ' ' + all_fname + ' >' + args.dirname + '/' + aligned_fname, shell=True)  # options=  # "--localpair --maxiterate 1000"

    # then rewrite aligned file with only new genes, converting to upper case and dots for gaps
    all_aligned_germlines = utils.read_germlines(args.dirname, only_region='v', aligned=True)
    with open(args.dirname + '/' + aligned_fname, 'w') as tmpfile:
        for gene, seq in all_aligned_germlines['v'].items():
            if gene not in all_new_genes:
                continue
            tmpfile.write('>%s\n%s\n' % (gene, seq.replace('-', '.').upper()))

    os.remove(old_aligned_fname)
    os.remove(missing_fname)
    os.remove(msa_table_fname)
    os.remove(all_fname)

# ----------------------------------------------------------------------------------------
def find_cyst_conversion_factor(known_cyst_positions, align_new_genes):

# ----------------------------------------------------------------------------------------
def write_cyst_file(known_cyst_positions):
    unaligned_genes = utils.read_germlines(args.dirname, only_region='v')
    aligned_genes = utils.read_germlines(args.dirname, only_region='v', aligned=True)
    cyst_positions = {}
    for gene, seq in unaligned_genes.items():
        

# ----------------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('ighv_fname', help='input germline v set (presumably a new one), in fasta')
parser.add_argument('--dirname', help='directory name for output (if not specified, we use <infname> with suffix removed)')
parser.add_argument('--reference-dir', default='data/imgt', help='directory with reference/old germline sets')
args = parser.parse_args()
if args.dirname is None:
    args.dirname = os.path.os.path.splitext(args.ighv_fname)[0]

files_to_copy = ['ighd.fasta', 'ighj.fasta', 'j_tryp.csv']
unaligned_fname = 'ighv.fasta'
aligned_fname = 'ighv-aligned.fasta'

# ----------------------------------------------------------------------------------------
# clean_dir()
# shutil.copyfile(args.ighv_fname, args.dirname + '/' + unaligned_fname)

# figure out which v genes we need to align
old_aligned_genes = utils.read_germlines(args.reference_dir, only_region='v', aligned=True)
all_new_genes = utils.read_germlines(args.dirname, only_region='v')  # all genes in ighv_fname, not just the new ones
genes_without_alignments = {}
for gene in all_new_genes['v']:
    if gene not in old_aligned_genes['v']:
        genes_without_alignments[gene] = all_new_genes['v'][gene]

# if len(genes_without_alignments) > 0:
#     align_new_genes(old_aligned_genes['v'], genes_without_alignments, all_new_genes['v'])

# for fname in files_to_copy:
#     shutil.copyfile(args.reference_dir + '/' + fname, args.dirname + '/' + fname)

known_cyst_positions = utils.read_cyst_positions(args.reference_dir)
write_cyst_file(known_cyst_positions)