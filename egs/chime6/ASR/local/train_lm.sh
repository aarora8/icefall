#!/usr/bin/env bash
export LC_ALL=C
echo "$0 $@"
[ -f path.sh ]  && . ./path.sh

echo "-------------------------------------"
echo "Building an SRILM language model     "
echo "-------------------------------------"


tgtdir=data/lm/
train_text=download/uppercase/lm_train_text
dev_text=download/uppercase/lm_dev_text
words_file=download/uppercase/lexicon.txt
oov_symbol="<UNK>"
for f in $words_file $train_text $dev_text; do
  [ ! -s $f ] && echo "No such file $f" && exit 1;
done

echo "Using train text: $train_text"
echo "Using dev text  : $dev_text"

# Extract the word list from the training dictionary; exclude special symbols
sort $words_file | awk '{print $1}' | grep -v '\#0' | grep -v '<eps>' | grep -v -F "$oov_symbol" > $tgtdir/vocab

ngram-count -lm $tgtdir/lm.gz -kndiscount1 -gt1min 0 -kndiscount2 -gt2min 1 -kndiscount3 -gt3min 2 -order 3 -text $train_text -vocab $tgtdir/vocab -unk -sort -map-unk "$oov_symbol"

ngram -order 3 -lm $tgtdir/lm.gz -unk -map-unk "$oov_symbol" -ppl $dev_text
