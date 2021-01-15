#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    echo "# Translating with checkpoint $checkpoint"
    base=$(basename $checkpoint)
    onmt_translate \
        -gpu 3 \
        -batch_size 16384 -batch_type tokens \
        -beam_size 5 \
        -model $checkpoint \
        -src data/wmt/UNv1.0.testset.en.sp \
        -tgt data/wmt/UNv1.0.testset.zh.sp \
        -output data/wmt/UNv1.0.testset.zh.hyp_${base%.*}.sp
done
