plink --vcf xxx.vcf --recode 12 transpose --output-missing-genotype 0 --allow-extra-chr --out xxx

parallel并行：
sample=$(ls *.vcf | awk -F '.' '{print $1}'); parallel -j 10 'echo {} && plink --vcf {}.vcf --recode 12 transpose --output-missing-genotype 0 --allow-extra-chr --out {}' ::: "${sample[@]}"

集群并行：
准备模板文件：echo "plink --vcf xxx.vcf --recode 12 transpose --output-missing-genotype 0 --allow-extra-chr --out xxx" > 3.0.transfer_vcf2emmax.sh
sample=$(ls *.vcf | awk -F '.' '{print $1}'); for i in ${sample}; do sed "s/xxx/${i}/g" 3.0.transfer_vcf2emmax.sh > ${i}.sh | chmod +x ${i}.sh; done

qsub提交：
sample=$(ls *.sh); for i in ${sample}; do qsub -l cpu=2:mem=20G --env -cwd ${i}; done
