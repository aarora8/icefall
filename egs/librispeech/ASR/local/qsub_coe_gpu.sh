#!/usr/bin/env bash

#$ -q gpu.q@@v100 -l gpu=1
#$ -wd /exp/aarora/icefall_work_env/icefall/egs/librispeech/ASR/
#$ -V
#$ -N train_job
#$ -j y -o $JOB_NAME
#$ -M ashish.arora.88888@gmail.com
#$ -m bea
#$ -l mem_free=30G
#$ -l h_rt=24:00:00
#$ -l hostname='!r8n04'

# big data config
# qsub -l gpu=4 -q gpu.q@@v100 -l h_rt=72:00:00
# #$ -m bea
# Activate dev environments and call programs

source ~/.bashrc
export PATH="/home/hltcoe/aarora/miniconda3/bin:$PATH"
conda activate icef

env| grep SGE_HGR_gpu
env | grep CUDA_VISIBLE_DEVICES
nvidia-smi

echo "$0: Running on `hostname`"
echo "$0: Started at `date`"
echo "$0: Running the job on GPU(s) $CUDA_VISIBLE_DEVICES"
"$@"

/home/hltcoe/aarora/miniconda3/envs/icef/bin/python3 tdnn_lstm_ctc/train.py
echo "$0: ended at `date`"
