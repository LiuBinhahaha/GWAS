#!/bin/bash
# tsv文件是处理后的表型文件
sample=$(ls *.tsv | awk -F '_' -v OFS="_" '{print $1,$2,$3}');

parallel --joblog log.out -j 12 'echo {} && ~/software/EMMAX/emmax-intel64 \
                                                        -t {} \
                                                        -o {}.ps \
                                                        -p {}_upper_traits.tsv \
                                                        -k {}.BN.kinf' ::: "${sample[@]}"
