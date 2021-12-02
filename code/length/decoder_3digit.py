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

# Switch to JSGF grammar
jsgf = Jsgf('ps_data/jsgf/digits.gram')
rule = jsgf.get_rule('digits.3digit')
fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
fsg.writefile('output/3digit.fsg')

decoder.set_fsg("3digit", fsg)
decoder.set_search("3digit")

hypos, refs = [], []
# Get all 3 digit files for man and woman category
speaker_groups = [r'SNR35dB/man/seq3digits_100_files/*.raw', r'SNR35dB/woman/seq3digits_100_files/*.raw']

for group in speaker_groups:
    for file in glob.glob(group):
	# Start decoding utterances
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
            hypos.append('_')

        with open(file.replace('raw', 'ref'), 'r') as ref_file:
            refs.append(ref_file.read().rstrip())
# Create hypotheses files
with open('results/length/3digit.hyp', 'w') as f:
    for hypo in hypos:
        f.write(f'{hypo}\n')
# Create references files
with open('results/length/3digit.ref', 'w') as f:
    for ref in refs:
        f.write(f'{ref}\n')
