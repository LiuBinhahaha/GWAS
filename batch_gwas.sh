#!/bin/bash

workdir=/vol/liubin/data/gwas/traits/

cd ${workdir}

traits=$(ls *.txt | awk -F '.' '{print $1}')

parallel --joblog ${workdir}/log.out -j 5 'echo {} && /home/liubin/software/EMMAX/emmax-intel64 \
                                                        -t /vol/liubin/data/gwas/test \
                                                        -o /vol/liubin/data/gwas/result/{}.ps \
                                                        -p /vol/liubin/data/gwas/traits/{}.txt \
                                                        -k /vol/liubin/data/gwas/emmax_test_kin \
                                                        -c /vol/liubin/data/gwas/cov.3.Q.txt' ::: "${traits[@]}"

