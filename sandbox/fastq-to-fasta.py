#! /usr/bin/env python
#
# This file is part of khmer, http://github.com/ged-lab/khmer/, and is
# Copyright (C) Michigan State University, 2009-2014. It is licensed under
# the three-clause BSD license; see doc/LICENSE.txt.
# Contact: khmer-project@idyll.org
#

"""
Convert FASTQ files to FASTA format.

% python sandbox/fastq-to-fasta.py [ -z -s ] <fastq_name>

Use '-h' for parameter help.
"""
import sys
import argparse
import os
import screed


def get_parser():
    parser = argparse.ArgumentParser(
        description='Convert fastq (.fq) files to fasta (.fa).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('input', help='The name of the input'
                        ' FASTQ sequence file.')
    parser.add_argument('-o', '--output', help='The name of the output'
                        ' FASTA sequence file.')
    parser.add_argument('-N', '--N_keep', default=False, action='store_true',
                        help='Option to drop reads'
                        ' containing \'N\'s.')
    return parser


def main():
    args = get_parser().parse_args()
    infile = args.input
    print('fastq from ', args.input)

    if args.output:
        write_out = open(args.output, 'w')

    N_count = 0
    for n, record in enumerate(screed.open(sys.argv[1])):
        if n % 10000 == 0:
            print>>sys.stderr, '...', n

        sequence = record['sequence']
        name = record['name']

        if 'N' in sequence:
            if not args.N_keep:
                N_count += 1
                continue
        if args.output:
            write_out.write('>' + name + '\n')
            write_out.write(sequence + '\n')
        else:
            print '>' + name
            print sequence

    print '\n' + 'lines from ' + args.input

    if not args.N_keep:
        print >> sys.stderr, str(N_count) + ' lines dropped.'

    else:
        print 'No lines dropped from file.'

if __name__ == '__main__':
    main()
