import re
file = open("/vol/liubin/data/gwas/part_test.vcf", 'r')
out = open("/vol/liubin/data/gwas/part_test.id.vcf", 'w')

for line in file:
    if line.startswith("#"):
        _line = line.rstrip()
        out.write(_line + '\n')
    else:
        _line = line.rstrip().split('\t')
        chr = _line[0].split('_')[1]
        ID = f'{chr}_{_line[1]}'
        out.write(chr + '\t' + _line[1] + '\t' + ID + '\t' + '\t'.join(_line[3:]) + '\n')

file.close()
out.close()
