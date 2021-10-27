export ICEFALL_ROOT=`pwd`/../../../
[ -f $ICEFALL_ROOT/tools/env.sh ] && . $ICEFALL_ROOT/tools/env.sh
export PYTHONPATH=`pwd`/../../..:$PYTHONPATH
export KALDI_ROOT=/exp/aarora/kaldi_work_env/kaldi_me/
export SRILM=/exp/aarora/kaldi_work_env/kaldi_me/tools/srilm
export PATH=$PATH:${SRILM}/bin/i686-m64:$ICEFALL_ROOT
export LC_ALL=C
