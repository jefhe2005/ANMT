#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    echo "$checkpoint"
    base=$(basename $checkpoint)
    sacrebleu data/wmt/UNv1.0.testset.zh < data/wmt/UNv1.0.testset.zh.hyp_${base%.*}
done
