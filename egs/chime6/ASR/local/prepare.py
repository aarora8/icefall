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
torch.set_num_threads(1)
torch.set_num_interop_threads(1)


def main():
    output_dir = Path('data/manifests')

    print('CHiME-6 manifest preparation:')
    chime_manifests = defaultdict(dict)
    eval_path = '/exp/aarora/kaldi_work_env/kaldi_me/egs/chime6/s5b_track1/data/eval_gss_hires_fork2'
    dev_path = '/exp/aarora/kaldi_work_env/kaldi_me/egs/chime6/s5b_track1/data/dev_gss_hires_fork2'
    train_path = '/exp/aarora/kaldi_work_env/kaldi_me/egs/chime6/s5b_track1/data/train_worn_simu_u400k_cleaned_trim_sp_hires_fork2'

    recording_set_eval, supervision_set_eval, feature_set_eval = lhotse.kaldi.load_kaldi_data_dir(eval_path, 16000, 0.01)
    recording_set_eval, supervision_set_eval = fix_manifests(
                recordings=RecordingSet.from_recordings(recording_set_eval),
                supervisions=SupervisionSet.from_segments(supervision_set_eval),
            )
    validate_recordings_and_supervisions(recording_set_eval, supervision_set_eval)
    cut_set = CutSet.from_manifests(recordings=recording_set_eval, supervisions=supervision_set_eval,
                                        features=feature_set_eval).trim_to_supervisions()

    #chime_manifests['eval']['cuts'] = cut_set
    chime_manifests['eval_gss'] = {
                'recordings': recording_set_eval,
                'supervisions': supervision_set_eval
            }
    cut_set.to_json(output_dir / f'cuts_chime_eval_gss_1.json.gz')
    supervision_set_eval.to_json(output_dir / f'supervisions_chime_eval_gss.json')
    recording_set_eval.to_json(output_dir / f'recordings_chime_eval_gss.json')

    recording_set_dev, supervision_set_dev, feature_set_dev = lhotse.kaldi.load_kaldi_data_dir(dev_path, 16000, 0.01)
    recording_set_dev, supervision_set_dev = fix_manifests(
                recordings=RecordingSet.from_recordings(recording_set_dev),
                supervisions=SupervisionSet.from_segments(supervision_set_dev),
            )
    validate_recordings_and_supervisions(recording_set_dev, supervision_set_dev)
    cut_set = CutSet.from_manifests(recordings=recording_set_dev, supervisions=supervision_set_dev,
                                        features=feature_set_dev).trim_to_supervisions()
    #chime_manifests['dev']['cuts'] = cut_set
    chime_manifests['dev_gss'] = {
                'recordings': recording_set_dev,
                'supervisions': supervision_set_dev
            }
    cut_set.to_json(output_dir / f'cuts_chime_dev_gss_1.json.gz')
    supervision_set_dev.to_json(output_dir / f'supervisions_chime_dev_gss.json')
    recording_set_dev.to_json(output_dir / f'recordings_chime_dev_gss.json')

    recording_set_train, supervision_set_train, feature_set_train = lhotse.kaldi.load_kaldi_data_dir(train_path, 16000, 0.01)
    recording_set_train, supervision_set_train = fix_manifests(
                recordings=RecordingSet.from_recordings(recording_set_train),
                supervisions=SupervisionSet.from_segments(supervision_set_train),
            )
    validate_recordings_and_supervisions(recording_set_train, supervision_set_train)
    cut_set = CutSet.from_manifests(recordings=recording_set_train, supervisions=supervision_set_train,
                                        features=feature_set_train).trim_to_supervisions()
    #chime_manifests['train']['cuts'] = cut_set
    chime_manifests['train'] = {
                'recordings': recording_set_train,
                'supervisions': supervision_set_train
            }
    cut_set.to_json(output_dir / f'cuts_chime_train_1.json.gz')
    supervision_set_train.to_json(output_dir / f'supervisions_chime_train.json')
    recording_set_train.to_json(output_dir / f'recordings_chime_train.json')

if __name__ == '__main__':
    main()
