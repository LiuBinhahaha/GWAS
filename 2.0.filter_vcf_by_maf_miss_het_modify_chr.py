#!/bin/Python-filter_maf_het.py

# 过滤maf missing het并修改染色体形式

import collections
import argparse
import gzip

# 创建解析器
parser = argparse.ArgumentParser(description="Filter VCF file based on MAF, heterozygosity, and missing rate.")

# 添加参数
parser.add_argument('-i', '--input', required=True, help="Input VCF file name")
parser.add_argument('-o', '--output', required=True, help="Output VCF file name")

# 解析参数
args = parser.parse_args()

file = open(args.input, 'r')
out = open(args.output, 'w')

for line in file:
    if line.startswith("#"):
        _line = line.rstrip()
        out.write(_line + '\n')
    else:
        allele = []  # statistic total allele
        line = line.rstrip().replace('|', '/')
        _line = line.split('\t')

        if len(_line[3]) == 1 and len(_line[4]) == 1:

            genotype_counts = collections.Counter()  # 字典计数
            for i in _line[9:]:
                tmp = i.split(':')[0]
                genotype_counts[tmp] += 1
                allele.append(tmp)

            count0 = genotype_counts.get('0/0', 0)
            count1 = genotype_counts.get('0/1', 0) + genotype_counts.get('1/0', 0)
            count2 = genotype_counts.get('1/1', 0)
            countn = genotype_counts.get('./.', 0)
            total = len(allele) - countn
            
            het = round(count1/total, 2)
        
            maf = round((2*count0+count1)/(2*total),2)

            missing = round(countn/len(allele), 2)

            if maf > 0.5:
                maf = 1 - maf
        
        # pic = 1 - ((maf)**2 + (1 - maf)**2)  # 双等位基因计算公式
        # pic = 1- ((maf)**2+(1-(maf))**2) - (2*(maf**2)*(1-maf)**2)  # 多allele计算公式

            if maf > 0.05 and missing < 0.1 and het < 0.05:
                # 染色体包含chr/scaffold_等字段的话执行：
                chr = _line[0].split('_')[1]
                id = f'{chr}:{_line[1]}'
                out.write(chr + '\t' + _line[1] + '\t' + id + '\t' + '\t'.join(_line[3:]) + '\n')

                # 如果染色体是纯数字：
                # out.write('\t'.join(_line[0:]) + '\n')

file.close()
out.close()
