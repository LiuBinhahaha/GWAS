import re
import os
import glob
import numpy as np
import argparse

def get_peak(snp_list, threshold, distance=100000):
    """
    递归获取一条染色体上的peak SNP
    :param snp_list: 字典，表示每个SNP的位置及其显著性值 {chrom: {snp_id: p-value}}
    :param threshold: 显著性阈值
    :param distance: 在递归中使用的基因组距离，用于确定上下游的范围
    :return: 返回所有满足条件的peak SNP及其对应的QTL区间
    """
    candidate_peaks = []
    candidate_qtls = []  # 存储每个峰及其对应的QTL区间

    # 若snp_list为空，则递归终止
    if not snp_list:
        return candidate_peaks, candidate_qtls

    for chrom, snps in snp_list.items():
        while snps:  # 若当前染色体上仍有未处理的SNP
            min_key = min(snps, key=snps.get)
            min_value = float(snps[min_key])

            # LD distance范围内是否至少有3个SNP
            tag = 0
            pos_min_key = int(min_key.split(':')[1])
            remove_keys = []
            candidate_snps = []

            for key in snps.keys():
                chrom, pos = key.split(':')
                if pos_min_key - distance <= int(pos) <= pos_min_key + distance:
                    tag += 1
                    remove_keys.append(key)
                    candidate_snps.append(int(pos))

            # 如果tag >= 3且该SNP的p-value <= threshold，则认为是一个peak
            if tag >= 3 and min_value <= threshold:
                candidate_peaks.append(f'{min_key}_{len(candidate_snps)}')
                # qtl
                qtl_interval = [min(candidate_snps),max(candidate_snps)]
                candidate_qtls.append([f'{min_key}_{len(candidate_snps)}', qtl_interval])
                # print(f"Peak SNP: {min_key}, QTL Interval: {qtl_interval}")

                for remove_key in remove_keys:
                    del snps[remove_key]
            else:
                # 若不满足条件，删除该最高峰，继续找下一个显著的SNP
                del snps[min_key]

    return candidate_qtls
    # return candidate_peaks


parser = argparse.ArgumentParser(description="Obtaining the qtl intervals and the number of significant loci of peak formation on each chromosome")

parser.add_argument('-i', '--input', required=True, help="Input pmap file name")
parser.add_argument('-o', '--output', required=True, help="Output peak qtl file name")
parser.add_argument('-r', '--significance_threshold', required=True, help="Please add the significance threshold")

args = parser.parse_args()

file = open(args.input, 'r')
out = open(args.output, 'w')
out.write('peak_snp_id' + ',' + 'start_qtl' + ',' + 'end_qtl' + ',' + 'snp_number_in_interval' + '\n')

threshold = float(args.significance_threshold)

snp_dic = {}
for line in file:
    if not line.startswith("ID"):
        _line = line.rstrip().split('\t')
        chrom, pos = _line[1], _line[2]
        p_value = float(_line[3])
        if chrom not in snp_dic:
            snp_dic[chrom] = {}

        # 保留显著性小于等于阈值的SNP
        if p_value <= threshold:
            snp_dic[chrom][_line[0]] = p_value


result = get_peak(snp_dic, threshold)

for i in result:
    print(i)
    out.write(i[0].split('_')[0] + ',' + str(i[1][0]) + ',' + str(i[1][1]) + ',' + i[0].split('_')[1] + '\n')

out.close()
