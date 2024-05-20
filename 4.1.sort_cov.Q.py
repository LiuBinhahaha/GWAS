fam = open("/vol/liubin/data/gwas/test.tfam", 'r')  # plink生成的tfam文件，提供样本名字
file = open("/vol/liubin/data/gwas/test.3.Q.txt", 'r')  # admixture生成的最佳分群下的Q文件
out = open("/vol/liubin/data/gwas/cov.3.Q.txt", 'w')  # 输出最佳分群数减1的Q-value

sample = []

for line in fam:
    _line = line.rstrip().split(' ')
    sample.append(_line[0])
fam.close()


for s, v in enumerate(file):
    _v = v.rstrip().split(' ')
    out.write(sample[s] + '\t' + sample[s] + '\t' +str(1) + '\t' + '\t'.join(_v[0:2]) + '\n')  # 协方差文件. 前两列是跟表型/tfam一样的个体名字。 第三列都是 1 (截距). 从第四列开始群体结构 Q1,Q2 ...(K-1)

file.close()
out.close()
