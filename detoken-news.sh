#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    base=$(basename $checkpoint)
    spm_decode \
        -model=data/wmt/wmtenzh.model \
        -input_format=piece \
        < data/wmt/test.zh.hyp_${base%.*}.sp \
        > data/wmt/test.zh.hyp_${base%.*}
done
