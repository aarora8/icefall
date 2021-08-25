#!/usr/bin/env python3

# Copyright (c)  2020  Xiaomi Corporation (authors: Junbo Zhang, Haowen Qiu)
# Apache 2.0
import argparse
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from collections import defaultdict

import torch
import lhotse
from lhotse import CutSet, Fbank, FbankConfig, LilcomHdf5Writer, combine
from lhotse import load_manifest
from lhotse.recipes import prepare_safet, prepare_musan
from lhotse.utils import fastcopy
from lhotse import validate_recordings_and_supervisions
from lhotse.audio import Recording, RecordingSet
from lhotse.supervision import SupervisionSegment, SupervisionSet
from lhotse.utils import Pathlike, check_and_rglob, recursion_limit
from snowfall.common import str2bool

# Torch's multithreaded behavior needs to be disabled or it wastes a lot of CPU and
# slow things down.  Do this outside of main() in case it needs to take effect
# even when we are not invoking the main (e.g. when spawning subprocesses).
torch.set_num_threads(1)
torch.set_num_interop_threads(1)


def locate_corpus(*corpus_dirs):
    for d in corpus_dirs:
        if os.path.exists(d):
            return d
    print("Please create a place on your system to put the downloaded Librispeech data "
          "and add it to `corpus_dirs`")
    sys.exit(1)


def get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--num-jobs',
        type=int,
        default=min(15, os.cpu_count()),
        help='number if cpu jobs')
    return parser


def main():
    args = get_parser().parse_args()
    output_dir = Path('data/manifests')

    print('safet manifest preparation:')
    safet_manifests = prepare_safet(
        corpus_dir='/exp/aarora/storage/corpora/safet/',
        output_dir=output_dir
    )

    sups = load_manifest('data/manifests/supervisions_safet_train.json')
    f = open('data/lm/lm_train_text', 'w')
    for s in sups:
        print(s.text, file=f)

    sups = load_manifest('data/manifests/supervisions_safet_dev.json')
    f = open('data/lm/lm_dev_text', 'w')
    for s in sups:
        print(s.text, file=f)

if __name__ == '__main__':
    main()

