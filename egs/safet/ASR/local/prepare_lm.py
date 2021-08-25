#!/usr/bin/env python
import logging
import subprocess
from pathlib import Path

from lhotse import load_manifest
from snowfall.common import setup_logger

def main():
    logging.info(f'Preparing LM training text.')
    lexicon =  'data/lm/librispeech-lexicon.txt'
    sups = load_manifest('data/manifests/supervisions_safet_train.json')
    f = open('data/lm/lm_train_text', 'w')
    for s in sups:
        print(s.text, file=f)

    sups = load_manifest('data/manifests/supervisions_safet_dev.json')
    f = open('data/lm/lm_train_text', 'w')
    for s in sups:
        print(s.text, file=f)

if __name__ == '__main__':
    main()
