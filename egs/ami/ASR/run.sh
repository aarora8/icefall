#!/usr/bin/env bash

# Copyright 2020 Xiaomi Corporation (Author: Junbo Zhang)
# Apache 2.0

# Example of how to build L and G FST for K2. Most scripts of this example are copied from Kaldi.

set -eou pipefail
. ./path.sh
. ./cmd.sh
stage=0
if [ $stage -le 0 ]; then
  local/prepare_dict.sh
fi

if [ $stage -le 1 ]; then
  local/prepare_lang.sh \
    --position-dependent-phones false \
    data/local/dict_nosp \
    "<UNK>" \
    data/local/lang_tmp_nosp \
    data/lang_nosp
fi

if [ $stage -le 2 ]; then
  utils/queue.pl --mem 30G --config conf/coe.conf exp/prepare.log ~/miniconda3/envs/icef/bin/python3 prepare.py
fi
exit
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

if [ $stage -le 4 ]; then
  utils/queue.pl --mem 20G --gpu 1 --config conf/coe.conf exp/train.log ~/miniconda3/envs/icef/bin/python3 mmi_bigram_train_1b.py
fi

if [ $stage -le 5 ]; then
  utils/queue.pl --mem 10G --gpu 1 --config conf/coe.conf exp/decode.log ~/miniconda3/envs/icef/bin/python3 mmi_bigram_decode.py --epoch 9
fi

