#!/bin/bash

for checkpoint in data/wmt/run/model_step*.pt; do
    echo "$checkpoint"
    base=$(basename $checkpoint)
    sacrebleu data/wmt/news-test-jieba.zh-og-557-cho12-alltags < data/wmt/test.zh-r.hyp_${base%.*}
done
