#!/usr/bin/env python3
import lhotse
import re
from lhotse import load_manifest

def main():
    sups = load_manifest('data/manifests/supervisions_chime_train.json')
    f = open('data/lm/lm_train_text', 'w')
    for s in sups:
        text = s.text
        text = text.upper()
        print(text, file=f)

    sups = load_manifest('data/manifests/supervisions_chime_dev_gss.json')
    f = open('data/lm/lm_dev_text', 'w')
    for s in sups:
        text = s.text
        text = text.upper()
        print(text, file=f)

if __name__ == '__main__':
    main()
