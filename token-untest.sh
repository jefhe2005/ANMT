#!/bin/bash

spm_encode --model=data/wmt/wmtenzh.model \
    < data/wmt/UNv1.0.testset.en \
    > data/wmt/UNv1.0.testset.en.sp
spm_encode --model=data/wmt/wmtenzh.model \
    < data/wmt/UNv1.0.testset.zh \
    > data/wmt/UNv1.0.testset.zh.sp