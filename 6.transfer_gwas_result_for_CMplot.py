file = open("/vol/liubin/data/gwas/test.qk.ps", 'r')
out = open("/vol/liubin/data/gwas/show_test.pmap", 'w')
out.write('ID' + '\t' + "chr" + '\t' + "pos" + '\t' + "p" + '\n')

for line in file:
    _line = line.rstrip().split('\t')
    chr = _line[0].rstrip().split('_')[0]
    pos = _line[0].rstrip().split('_')[1]
    out.write(_line[0] + '\t' + chr + '\t' + pos + '\t' + _line[3] + '\n')

file.close()
out.close()
