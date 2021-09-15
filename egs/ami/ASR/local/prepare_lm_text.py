#!/usr/bin/env python3
import lhotse
import re
from lhotse import load_manifest

WORDLIST = dict()

#def read_lexicon_words(lexicon):
#    with open(lexicon, 'r', encoding='utf-8') as f:
#        for line in f:
#            parts = line.strip().split()
#            word = parts[0]
#            WORDLIST[word] = 1
#
#def process_transcript(transcript):
#    global WORDLIST
#    if_only_unk = True
#    # https://www.programiz.com/python-programming/regex
#    # [] for set of characters you with to match
#    # eg. [abc] --> will search for a or b or c
#    # "." matches any single character
#    # "$" to check if string ends with a certain character 
#    # eg. "a$" should end with "a"
#    # replace <extreme background> with <extreme_background>
#    # replace <foreign lang="Spanish">fuego</foreign> with foreign_lang=
#    # remove "[.,!?]"
#    # remove " -- "
#    # remove " --" --> strings that ends with "-" and starts with " "
#    # \s+ markers are – that means “any white space character, one or more times”
#    tmp = re.sub(r'<extreme background>', '', transcript)
#    tmp = re.sub(r'<background>', '', transcript)
#    tmp = re.sub(r'foreign\s+lang=', 'foreign_lang=', tmp)
#    tmp = re.sub(r'\(\(', '', tmp)
#    tmp = re.sub(r'\)\)', '', tmp)
#    tmp = re.sub(r'[.,!?]', ' ', tmp)
#    tmp = re.sub(r' -- ', ' ', tmp)
#    tmp = re.sub(r' --$', '', tmp)
#    list_words = re.split(r'\s+', tmp)
#
#    out_list_words = list()
#    for w in list_words:
#        w = w.strip()
#        w = w.upper()
#        if w == "":
#            continue
#        elif w in WORDLIST:
#            out_list_words.append(w)
#            if_only_unk = False
#        else:
#            out_list_words.append('<UNK>')
#
#    if if_only_unk:
#        out_list_words = ''
#    return ' '.join(out_list_words)


def main():
    #read_lexicon_words('data/lm/librispeech-lexicon.txt')
    sups = load_manifest('data/manifests/supervisions_train.json')
    f = open('data/lm/lm_train_text', 'w')
    for s in sups:
        #text = process_transcript(s.text)
        print(s.text, file=f)

    sups = load_manifest('data/manifests/supervisions_dev.json')
    f = open('data/lm/lm_dev_text', 'w')
    for s in sups:
        #text = process_transcript(s.text)
        print(s.text, file=f)

if __name__ == '__main__':
    main()
