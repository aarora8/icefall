#!/usr/bin/env python3
import lhotse
from lhotse import load_manifest

WORDLIST = dict()
UNK = '<UNK>'
REPLACE_UNKS = True

def process_transcript(transcript):
    global WORDLIST
    if_only_unk = True
    # https://www.programiz.com/python-programming/regex
    # [] for set of characters you with to match
    # eg. [abc] --> will search for a or b or c
    # "." matches any single character
    # "$" to check if string ends with a certain character 
    # eg. "a$" should end with "a"
    # replace <extreme background> with <extreme_background>
    # replace <foreign lang="Spanish">fuego</foreign> with foreign_lang=
    # remove "[.,!?]"
    # remove " -- "
    # remove " --" --> strings that ends with "-" and starts with " "
    # \s+ markers are – that means “any white space character, one or more times”
    tmp = re.sub(r'<extreme background>', '', transcript)
    tmp = re.sub(r'<background>', '', transcript)
    tmp = re.sub(r'foreign\s+lang=', 'foreign_lang=', tmp)
    tmp = re.sub(r'\(\(', '', tmp)
    tmp = re.sub(r'\)\)', '', tmp)
    tmp = re.sub(r'[.,!?]', ' ', tmp)
    tmp = re.sub(r' -- ', ' ', tmp)
    tmp = re.sub(r' --$', '', tmp)
    list_words = re.split(r'\s+', tmp)

    out_list_words = list()
    for w in list_words:
        w = w.strip()
        w = w.upper()
        if w == "":
            continue
        elif w in WORDLIST:
            out_list_words.append(w)
            if_only_unk = False
        else:
            out_list_words.append(UNK)

    if if_only_unk:
        out_list_words = ''
    return ' '.join(out_list_words)


def read_lexicon_words(lexicon):
    with open(lexicon, 'r', encoding='utf-8') as f:
        for line in f:
            line = re.sub(r'(?s)\s.*', '', line)
            WORDLIST[line] = 1

sups = load_manifest('exp/data/supervisions_safet_train.json')
f = open('exp/data/lm_train_text', 'w')
for s in sups:
    print(s.text, file=f)

sups = load_manifest('exp/data/supervisions_safet_dev_clean.json')
f = open('exp/data/lm_dev_text', 'w')
for s in sups:
    print(s.text, file=f)
