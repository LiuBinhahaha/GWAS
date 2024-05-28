import glob
import re
import os

fs = glob.glob("/vol/liubin/data/gwas/result/*.ps")

for files in fs:
    file_name = os.path.basename(files).split(".")[0]
    print(file_name)
    out = open(f'/vol/liubin/data/gwas/result/{file_name}.pmap', "w")
    out.write('ID\tchr\tpos\tp\n')

    file = open(files, 'r')
    for line in file:
        _line = line.rstrip().split('\t')
        chr = _line[0].split('_')[0]
        pos = _line[0].split("_")[1]
        id = _line[0]
        p = _line[3]
        out.write(id + '\t' + chr + '\t' + pos + '\t' + p + '\n')
    file.close()
    out.close()
    
