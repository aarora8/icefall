#!/usr/bin/env bash

# Copyright 2020 Xiaomi Corporation (Author: Junbo Zhang)
# Apache 2.0
# Example of how to build L and G FST for K2. Most scripts of this example are copied from Kaldi.

set -eou pipefail
. ./local/path.sh
. ./local/cmd.sh
stage=3
if [ $stage -le 0 ]; then
  mkdir -p data/lm data/manifests
  local/queue.pl --mem 30G --config local/coe.conf data/prepare.log ~/miniconda3/envs/icef/bin/python3 prepare.py
fi

if [ $stage -le 3 ]; then
  echo "LM preparation"
  local/prepare_lm.py
  local/train_lm_srilm.sh
  gunzip -c data/local/lm/lm.gz >data/local/lm/lm_tgmed.arpa

  python3 -m kaldilm \
    --read-symbol-table="data/lang_nosp/words.txt" \
    --disambig-symbol='#0' \
    --max-order=3 \
    data/local/lm/lm_tgmed.arpa >data/lang_nosp/G.fst.txt
fi
