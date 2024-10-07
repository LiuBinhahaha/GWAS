# 利用EMMAX提供的脚本计算亲缘关系矩阵

~/software/EMMAX/emmax-kin-intel64 xxx -v -d 10 -o xxx.BN.kinf
# xxx是上一步plink转化的tped、tmap文件，这里不需要加文件后缀

# parallel并行：
sample=$(ls *.tped | awk -F '.' '{print $1}'); parallel -j 10 'echo {} && ~/software/EMMAX/emmax-kin-intel64 {} -v -d 10 -o {}.BN.kinf' ::: "${sample[@]}"

# run in cluster
准备脚本模板：
echo "~/software/EMMAX/emmax-kin-intel64 xxx -v -d 10 -o xxx.BN.kinf" > 4.0.calu_kinship.sh
sample=$(ls *.tped | awk -F '.' '{print $1}'); for i in ${sample}; do sed "s/xxx/${i}/g" 4.0.calu_kinship.sh > calu_kinship_${i}.sh | chmod +x calu_kinship_${i}.sh; done

qsub提交：
sample=$(ls *.sh); for i in ${sample}; do qsub -l cpu=2:mem=20G --env -cwd ${i}; done
