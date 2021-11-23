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
rule = jsgf.get_rule('digits.1digit')
fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
fsg.writefile('output/1digit.fsg')

decoder.set_fsg("1digit", fsg)
decoder.set_search("1digit")

hypos, refs = [], []

for file in glob.glob(r'SNR35dB/man/seq1digit_200_files/*.raw'):
    decoder.start_utt()
    stream = open(file, 'rb')
    while True:
        buf = stream.read(1024)
        if buf:
             decoder.process_raw(buf, False, False)
        else:
             break
    decoder.end_utt()

    hypothesis = decoder.hyp()

    if hypothesis and hypothesis.hypstr:
        hypos.append(hypothesis.hypstr)
    else:
        hypos.append('_')

    with open(file.replace('raw', 'ref'), 'r') as ref_file:
        refs.append(ref_file.read().rstrip())

with open('results/lang_mod/1digit.hyp', 'w') as f:
    for hypo in hypos:
        f.write(f'{hypo}\n')

with open('results/lang_mod/1digit.ref', 'w') as f:
    for ref in refs:
        f.write(f'{ref}\n')
