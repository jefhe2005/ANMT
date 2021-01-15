#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    echo "$checkpoint"
    base=$(basename $checkpoint)
    sacrebleu data/wmt/UNv1.0.testset.zh-og < data/wmt/UNv1.0.testset.zh-r.hyp_${base%.*}
done
