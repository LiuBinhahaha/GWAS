#!/bin/bash
# 从大群体中提取目标样本的vcf文件，基因型文件的样本数一定与表型文件的样本数保持一致，并对提取出来的小群体做质控。
bcftools index 1844_0.05_0.1_snps_ID.vcf.gz

bcftools view 1844_0.05_0.1_snps_ID.vcf.gz -S 499.sample > 499_sample.vcf

# parallel并行提取多个小群体的vcf文件：
sample=$(ls *.sample | awk -F '.' '{print $1}'); parallel -j 'echo {} && bcftools view 1844_0.05_0.1_snps_ID.vcf.gz -S {} > {}.vcf' ::: "${sample[@]}"

# 集群批量提取
准备提取模板：echo "bcftools view 1844_0.05_0.1_snps_ID.vcf.gz -S xxx > xxx.vcf" > extract_vcf.sh
sample=$(ls *.sample | awk -F '.' '{print $1}'); for i in ${sample}; do sed "s/xxx/${i}/g" exreact_vcf.sh > ${i}.sh; done
