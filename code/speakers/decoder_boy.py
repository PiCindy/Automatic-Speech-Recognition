#!/usr/bin/python

from os import environ, path
from sys import stdout
import glob
from pocketsphinx import *
from sphinxbase import *

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
config.set_string('-dict', 'ps_data/lex/digits.dic')
decoder = Decoder(config)

seq_lengths = ['1digit', '3digit', '5digit']
# Get all files from boy category (SNR35dB)
folders = [r'SNR35dB/boy/seq1digit_200_files/*.raw', r'SNR35dB/boy/seq3digits_100_files/*.raw', r'SNR35dB/boy/seq5digits_100_files/*.raw']
# Erase previous data
open('results/speakers/boy.hyp', 'w').close()
open('results/speakers/boy.ref', 'w').close()

for seq, folder in zip(seq_lengths, folders):

    # Switch to JSGF grammar
    jsgf = Jsgf('ps_data/jsgf/digits.gram')
    rule = jsgf.get_rule('digits.'+seq)
    fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
    fsg.writefile('output/'+seq+'.fsg')

    decoder.set_fsg(seq, fsg)
    decoder.set_search(seq)

    hypos, refs = [], []

    for file in glob.glob(folder):
    	# Start decoding
        decoder.start_utt()
        stream = open(file, 'rb')
        while True:
            buf = stream.read(1024)
            if buf:
                 decoder.process_raw(buf, False, False)
            else:
                 break
        decoder.end_utt()
	# Create hypotheses
        hypothesis = decoder.hyp()

        if hypothesis and hypothesis.hypstr:
            hypos.append(hypothesis.hypstr)
        else:
            hypos.append('')

        with open(file.replace('raw', 'ref'), 'r') as ref_file:
            refs.append(ref_file.read().rstrip())
    # Create hypotheses files
    with open('results/speakers/boy.hyp', 'a') as f:
        for hypo in hypos:
            f.write(f'{hypo}\n')
        f.write('\n')
    # Create references files
    with open('results/speakers/boy.ref', 'a') as f:
        for ref in refs:
            f.write(f'{ref}\n')
        f.write('\n')
