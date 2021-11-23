#!/usr/bin/python

from os import environ, path
import glob

from pocketsphinx import *
from sphinxbase import *


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/en-us.lm.bin')
config.set_string('-dict', 'ps_data/lex/digits.dic')

# Decode streaming data.
decoder = Decoder(config)
hypos, refs = [], []

for file in glob.glob(r'SNR35dB/man/*/*.raw'):
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
    logmath = decoder.get_logmath()
    hypos.append(hypothesis.hypstr)

    with open(file.replace('raw', 'ref'), 'r') as ref_file:
        refs.append(ref_file.read().rstrip())

with open('results/lang_mod/digits_ngram.hyp', 'w') as f:
    for hypo in hypos:
        f.write(f'{hypo}\n')

with open('results/lang_mod/digits_ngram.ref', 'w') as f:
    for ref in refs:
        f.write(f'{ref}\n')
