import re
import os
import glob
import numpy as np
import subprocess
import time

# 获取gwas结果的peak snp；提取peak snp上游50k，下游100k的vcf文件; 画LD block图

fs = glob.glob("/vol/liubin/data/NG_1844_selection_analysis/gwas/SNP/*.ps.txt")

for files in fs:
    file_name = os.path.basename(files).split('.')[0]
    
    # 输出lead snp信息用于ShowLDSVG
    out = open(f"/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}.lead_snp", 'w')
    
    # 输出LDBlockShow的脚本
    out2 = open(f"/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}.sh", 'w')

    tag = 0
    file = open(files, 'r')
    for line in file:
        if not line.startswith("SNP"):
            tag += 1

    threshold = np.absolute(np.log10(0.05/int(tag)))
    print(f'{file_name}阈值: {threshold}')

    file.seek(0, 0)
    tmp = []
    for line in file:
        if not line.startswith("SNP"):
            _line = line.rstrip().split('\t')
            p_value = np.absolute(np.log10(float(_line[3])))
            if p_value >= threshold:
                tmp.append([f'scaffold_{_line[1]}', _line[2], p_value])
    p = []
    for v in tmp:
        if re.search(r'scaffold_2', v[0]):  # 仅保留scaffold_2
            p.append(v[2])

    P_extre = np.max(p)
    print(f'{file_name}p极值: {P_extre}')

    lead_snp = '-'
    for k in tmp:
        if P_extre in k:
            lead_snp = f'{k[0]}:{k[1]}'
            
            # 输出lead snp信息
            out.write(k[0] + '\t' + k[1] + '\t' + 'lead' + '\n')

    print(f'{file_name}lead_snp: {lead_snp}')

    # lead SNP 上游50k，下游100k作为分析区间
    lead_snp_chr = lead_snp.split(':')[0]
    lead_snp_pos_up = int(lead_snp.split(':')[1]) - 50000
    lead_snp_pos_down = int(lead_snp.split(':')[1]) + 100000
    print(file_name, lead_snp_chr, lead_snp_pos_up, lead_snp_pos_down)
    
    # 获取peak snp的vcf文件
    bcftools_command = [
        'bcftools', 'view', 
        '-r', f'{lead_snp_chr}:{lead_snp_pos_up}-{lead_snp_pos_down}', 
        '/vol/liubin/data/NG_1844_selection_analysis/1844_0.05_0.1_snps.vcf.gz', 
        '-o', f'/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}.vcf.gz'
    ]
    subprocess.run(bcftools_command, check=True)


    bcftools_index = [
        'bcftools', 'index', f'/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}.vcf.gz',
    ]
    subprocess.run(bcftools_index, check=True)


    # 仅保留c1-c3亚群的变异信息
    bcftools_filter_c1_c3 = [
        'bcftools', 'view', f'/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}.vcf.gz', 
        '-S', '/vol/liubin/data/NG_1844_selection_analysis/c1-c3.txt', '--force-samples', 
        '-o', f'/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}_c1-c3.vcf'
    ]
    subprocess.run(bcftools_filter_c1_c3, check=True)

    # LD_blocK_show
    LD_block_show_command = [
        'LDBlockShow', '-InVCF', f'/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}_c1-c3.vcf', 
        '-OutPut', f'/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}', 
        '-SpeSNPName', f"/vol/liubin/data/NG_1844_selection_analysis/gwas/{file_name}.lead_snp", 
        '-Region', f'{lead_snp_chr}:{lead_snp_pos_up}:{lead_snp_pos_down}', 
        '-OutPdf', '-SeleVar', '2'
    ]
    # print("Running command:", " ".join(LD_block_show_command))
    try:
        subprocess.run(LD_block_show_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Warning: {file_name} ShowLDSVG failed with error: {e}')
    
    out2.write(" ".join(LD_block_show_command))
    # 运行到此，发现直接运行这个脚本执行LDBlockShow命令会出现图中没有标注lead snp，但是直接把程序输出的命令直接输入终端是可以在图中标出lead snp、
    # 所以就将LDBlockShow命令输出到.shell脚本中，从外部再次运行

    time.sleep(2)

    print(f'{file_name} done !')
    print('')
    print('')


# sample=$(ls *.sh); for i in ${sample}; do bash ${i}; done
