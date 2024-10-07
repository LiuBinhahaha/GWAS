# GWAS

## PVE计算公式
![image](https://github.com/LiuBinhahaha/Figs/blob/main/GWAS/maf.png)

GWAS通过分析case/control组之间的差异来寻找与疾病关联的SNP位点，然而case和control两组之间，可能本身就存在一定的差异，会影响关联分析的检测。
Population stratification,称之为群体分层，是最常见的差异来源，指的是case/control组的样本来自于不同的祖先群体，其分型结果自然是有差异的。GWAS分析的目的是寻找由于疾病导致的差异，其他的差异都属于系统误差，在进行分析时，需要进行校正。
对于群体分层的校正，通常采主成分分析的方法，即PCA。

EMMAX接受的vcf文件格式(染色体仅用数字表示)：
1      32473   1:32473       G       C       108106  PASS    .       GT:AD:DP:GQ:PGT:PID:PL  0/0:5,0:5:15:.:.:0,15,168       0/0:11,0:11:33:.:.:0,33,407     0/0:7,0:7:21:.:.:0,21,248
