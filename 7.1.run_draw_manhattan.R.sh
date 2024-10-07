# parallel运行：
# 运行前在8.0中修改Rscript的路径到目标路径中。

sample=$(ls *.pmap | awk -F '.' '{print $1}'); parallel -j 20 'echo {} && Rscript 8.0.draw_manhattan.R {}.pmap {}' ::: "${sample[@]}"
