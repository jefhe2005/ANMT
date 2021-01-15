#!/bin/bash

spm_encode --model=data/wmt/wmtenzh.model \
    < data/wmt/test.en \
    > data/wmt/test.en.sp
spm_encode --model=data/wmt/wmtenzh.model \
    < data/wmt/test.zh \
    > data/wmt/test.zh.sp