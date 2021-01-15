#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    echo "# Translating with checkpoint $checkpoint"
    base=$(basename $checkpoint)
    onmt_translate \
        -gpu 7 \
        -batch_size 16384 -batch_type tokens \
        -beam_size 5 \
        -model $checkpoint \
        -src data/wmt/test.en.sp \
        -tgt data/wmt/test.de.sp \
        -output data/wmt/test.de.hyp_${base%.*}.sp
done
