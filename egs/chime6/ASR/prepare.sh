#!/usr/bin/env bash
export PYTHONPATH=/exp/aarora/icefall_work_env/icefall:$PYTHONPATH
source utils/activate_k2_release.sh
set -eou pipefail

nj=15
stage=-1
stop_stage=100
dl_dir=$PWD/download
. shared/parse_options.sh || exit 1
. ./local/path.sh || exit 1
vocab_sizes=(
  5000
  2000
  1000
  500
)
mkdir -p data

log() {
  local fname=${BASH_SOURCE[1]##*/}
  echo -e "$(date '+%Y-%m-%d %H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}

log "dl_dir: $dl_dir"

if [ $stage -le 1 ] && [ $stop_stage -ge 1 ]; then
  log "Stage 1: Prepare CHiME manifest"
  mkdir -p data/manifests
  local/queue.pl --mem 30G --config local/coe.conf data/prepare.log ~/miniconda3/envs/k2/bin/python3 local/prepare2.py
fi

if [ $stage -le 2 ] && [ $stop_stage -ge 2 ]; then
  log "Stage 2: Prepare musan manifest"
  mkdir -p data/manifests
  lhotse prepare musan $dl_dir/musan data/manifests
fi

#if [ $stage -le 3 ] && [ $stop_stage -ge 3 ]; then
#  log "Stage 3: Compute fbank for CHiME"
#  mkdir -p data/fbank
#  local/queue.pl --mem 30G --config local/coe.conf data/fbank.log ~/miniconda3/envs/k2/bin/python3 local/compute_fbank_chime.py
#fi

if [ $stage -le 4 ] && [ $stop_stage -ge 4 ]; then
  log "Stage 4: Compute fbank for musan"
  mkdir -p data/fbank
  ./local/compute_fbank_musan.py
fi


if [ $stage -le 5 ] && [ $stop_stage -ge 5 ]; then
  log "Stage 5: Prepare phone based lang"
  lang_dir=data/lang_phone
  mkdir -p $lang_dir
  mkdir -p data/lm

  cp download/uppercase/lexicon.txt $lang_dir/lexicon.txt
  if [ ! -f $lang_dir/L_disambig.pt ]; then
    ./local/prepare_lang.py --lang-dir $lang_dir
  fi

  local/prepare_lm_text.py
  local/train_lm.sh
fi

if [ $stage -le 6 ] && [ $stop_stage -ge 6 ]; then
  log "State 6: Prepare BPE based lang"

  for vocab_size in ${vocab_sizes[@]}; do
    lang_dir=data/lang_bpe_${vocab_size}
    mkdir -p $lang_dir
    # We reuse words.txt from phone based lexicon
    # so that the two can share G.pt later.
    cp data/lang_phone/words.txt $lang_dir
    if [ ! -f $lang_dir/train.txt ]; then
      log "Generate data for BPE training"
      cat download/uppercase/lm_train_text > $lang_dir/transcript_words.txt
    fi

    ./local/train_bpe_model.py \
      --lang-dir $lang_dir \
      --vocab-size $vocab_size \
      --transcript $lang_dir/transcript_words.txt

    if [ ! -f $lang_dir/L_disambig.pt ]; then
      ./local/prepare_lang_bpe.py --lang-dir $lang_dir
    fi
  done
fi

if [ $stage -le 7 ] && [ $stop_stage -ge 7 ]; then
  log "Stage 7: Prepare bigram P"

  for vocab_size in ${vocab_sizes[@]}; do
    lang_dir=data/lang_bpe_${vocab_size}

    if [ ! -f $lang_dir/transcript_tokens.txt ]; then
      ./local/convert_transcript_words_to_tokens.py \
        --lexicon $lang_dir/lexicon.txt \
        --transcript $lang_dir/transcript_words.txt \
        --oov "<UNK>" \
        > $lang_dir/transcript_tokens.txt
    fi

    if [ ! -f $lang_dir/P.arpa ]; then
      ./shared/make_kn_lm.py \
        -ngram-order 2 \
        -text $lang_dir/transcript_tokens.txt \
        -lm $lang_dir/P.arpa
    fi

    if [ ! -f $lang_dir/P.fst.txt ]; then
      python3 -m kaldilm \
        --read-symbol-table="$lang_dir/tokens.txt" \
        --disambig-symbol='#0' \
        --max-order=2 \
        $lang_dir/P.arpa > $lang_dir/P.fst.txt
    fi
  done
fi

if [ $stage -le 8 ] && [ $stop_stage -ge 8 ]; then
  log "Stage 8: Prepare G"
  gunzip -c data/lm/lm.gz > data/lm/lm.arpa
  python3 -m kaldilm \
    --read-symbol-table="data/lang_phone/words.txt" \
    --disambig-symbol='#0' \
    --max-order=3 \
    data/lm/lm.arpa > data/lm/G_3_gram.fst.txt
fi

if [ $stage -le 9 ] && [ $stop_stage -ge 9 ]; then
  log "Stage 9: Compile HLG"
  ./local/compile_hlg.py --lang-dir data/lang_phone

  for vocab_size in ${vocab_sizes[@]}; do
    lang_dir=data/lang_bpe_${vocab_size}
    ./local/compile_hlg.py --lang-dir $lang_dir
  done
fi

# local/queue.pl --mem 30G --gpu 2 --config local/coe.conf tdnn_lstm_ctc/exp/train.log ~/miniconda3/envs/k2/bin/python3 ./tdnn_lstm_ctc/train.py
# local/queue.pl --mem 35G --gpu 1 --config local/coe.conf data/decode.log ~/miniconda3/envs/k2/bin/python3 ./tdnn_lstm_ctc/decode.py
