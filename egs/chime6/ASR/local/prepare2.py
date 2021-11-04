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
from lhotse import load_manifest, fix_manifests
from lhotse.recipes import prepare_ami, prepare_musan
from lhotse.utils import fastcopy
from lhotse import validate_recordings_and_supervisions
from lhotse.audio import Recording, RecordingSet
from lhotse.supervision import SupervisionSegment, SupervisionSet
from lhotse.features import FeatureSet
from lhotse.utils import Pathlike, check_and_rglob, recursion_limit
from lhotse.recipes import prepare_chime
from icefall.utils import get_executor
def main():
    output_dir = Path('data/manifests')
    corpus_dir = Path('/exp/aarora/CHiME6_data_prep/CHiME6/')
    print('CHiME-6 manifest preparation:')
    chime_manifests = prepare_chime(
        corpus_dir=corpus_dir,
        output_dir=output_dir
    )
    num_jobs = min(50, os.cpu_count())
    num_mel_bins = 80
    extractor = Fbank(FbankConfig(num_mel_bins=num_mel_bins))
    with get_executor() as ex:  # Initialize the executor only once.
        for partition, m in chime_manifests.items():
            print(partition)
            print(m)
            recording_set, supervision_set = fix_manifests(
                    recordings=RecordingSet.from_recordings(m["recordings"]),
                    supervisions=SupervisionSet.from_segments(m["supervisions"])
                )
            cut_set = CutSet.from_manifests(
                    recordings=recording_set,
                    supervisions=supervision_set,
                ).trim_to_supervisions(keep_overlapping=False)

            #cut_set.to_json(output_dir / f'cuts_chime_{partition}_1.json.gz')
            cut_set = cut_set.compute_and_store_features(
                    extractor=extractor,
                    storage_path=f"data/fbank/feats_{partition}",
                    num_jobs=num_jobs if ex is None else 80,
                    executor=ex,
                    storage_type=LilcomHdf5Writer,
                )
            cut_set.to_json(output_dir / f"cuts_{partition}.json.gz")
if __name__ == '__main__':
    main()
