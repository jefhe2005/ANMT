#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    echo "$checkpoint"
    base=$(basename $checkpoint)
    sacrebleu data/wmt/en-de-test.de-og-1065-alltags < data/wmt/test.de-r.hyp_${base%.*}
done
