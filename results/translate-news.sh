#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    echo "# Translating with checkpoint $checkpoint"
    base=$(basename $checkpoint)
    onmt_translate \
        -gpu 0 \
        -batch_size 16384 -batch_type tokens \
        -beam_size 5 \
        -model $checkpoint \
        -src data/wmt/test.en.sp \
        -tgt data/wmt/test.zh.sp \
        -output data/wmt/test.zh.hyp_${base%.*}.sp
done
