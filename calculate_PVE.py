import numpy as np
import re
import os
import glob
import collections

vcf = open("/vol/liubin/data/gwas/test_test_id.vcf", 'r')
fs = glob.glob("/vol/liubin/data/gwas/result/*.ps")

dic = {}
for line in vcf:
    if line.startswith("#"):
        continue
    else:
        allele = []
        _line = line.rstrip().split('\t')
        if _line[2] not in dic:
            dic[_line[2]] = []  # 存放所有位点的maf

        genotype_count = collections.Counter()  # 字典计数
        for i in _line[9:]:
            tmp = i.strip().split(':')[0]
            allele.append(tmp)
            genotype_count[tmp] += 1
            
        count0 = genotype_count.get('0/0', 0)
        count1 = genotype_count.get('0/1', 0) + genotype_count.get('1/0', 0)
        count2 = genotype_count.get('1/1', 0)
        countn = genotype_count.get('./.', 0)
        total = len(allele) - countn
        maf = round((2*count0+count1)/(2*total),2)
        if maf > 0.5:
            maf = 1 - maf
        dic[_line[2]] += round(maf, 2), total  # 字典值中第一个数是maf，第二个数是该SNP/variant参与分析的样本数
vcf.close()

print(dic['1_4594'])

for files in fs:
    _traits = os.path.basename(files)
    traits = _traits.split('.')[0]
    out = open(f'/vol/liubin/data/gwas/result/{traits}.PVE', 'w')

    file = open(files, 'r')
    for l in file:
        _l = l.rstrip().split('\t')
        id = _l[0]
        if id in dic:
            MAF, n = dic[id]  # n GWAS中该SNP参与分析的个体数
            effect = float(_l[1])  # 效应值β
            se = float(_l[2])  # GWAS结果的标准误se
            denominator = 2 * effect ** 2 * MAF * (1 - MAF) + (se * effect) ** 2 * 2 * n * MAF * (1 - MAF)
            if denominator != 0:
                PVE = (2 * effect ** 2 * MAF * (1 - MAF)) / denominator
            else:
                PVE = 0
            out.write('\t'.join(_l) + '\t' + str(PVE) + '\n')
    
    out.close()
    file.close()


