# GWAS
emmax-GWAS
1. vcf file add id

2. transfer format to p-file(tped, tmap, tfam...)
   plink --vcf test.vcf --recode 12 transpose --output-missing-genotype 0 --allow-extra-chr --out test 

   emmax可接受plink长格式
   基因型需要先 imputation（填充可以使用beagle），不能有缺失，缺失可用0代替（相当于用0填充 output-missing-genotype 0），且只识别双等位位点
   --output-missing-genotype 0  缺失基因型用0代替
   --transpose 转置

3. emmax-kin计算亲缘关系（也可使用GCTA或Tassel计算的亲缘关系）
   emmax-kin-intel64 /vol/liubin/data/gwas/test -v -d 10 -o /vol/liubin/data/gwas/test.BN.kinf
    explain：
    -o [outf] : output file name (default is [tpedf].[aBN or aIBS].kinf
    -w [weightf] : weight for each SNP
    -d [# digits]  : precision of the kinship values (default : 10)  亲缘关系值精度
    -M [float] : maximum memory in GB (default: 4.0) 内存大小
    -s : compute IBS kinship matrix (default is Balding-Nicholas)  IBS亲缘关系，默认BN
    -v : turn on verbose mode  详细模式
    -r : randomly fill missing genotypes (default is imputation by average)  填充基因型缺失值，默认使用平均值
    -x : include non-autosomal chromosomes in computing kinship matrices
    -S [int] : set random seed 随机数
    -m [float] : MAF threshold (default is 0)  maf
    -c [float] : Call rate threshold (default is 0)

## PVE计算公式
![image](GWAS/maf.png)
