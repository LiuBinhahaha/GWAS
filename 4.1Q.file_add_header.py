vcf = open("/vol/liubin/data/gwas/part_test.id.vcf", 'r')
file = open("/vol/liubin/data/gwas/test.3.Q.txt", 'r')
out = open("/vol/liubin/data/gwas/add_header.3.Q.txt", 'w')

sample = []

for line in vcf:
    if line.startswith("#"):
        if line.startswith("#CHROM"):
            _line = line.rstrip().split('\t')
            for i in _line[9:]:
                sample.append(i)
    else:
        break
vcf.close()

out.write("<Covariate>" + '\n')
out.write("<Individuals>" + '\t' + 'Q1' + '\t' + 'Q2' + '\n')  # 这里已经删除Q3

for s, v in enumerate(file):
    _v = v.rstrip().split(' ')
    out.write(sample[s] + '\t' + '\t'.join(_v[0:2]) + '\n')

file.close()
out.close()
