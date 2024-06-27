# 获取命令行参数
args <- commandArgs(trailingOnly = TRUE)

# 检查是否提供了必要的参数
if (length(args) != 2) {
  stop("请提供输入文件和输出文件名！\n用法: Rscript xxx.R 输入文件 输出文件")
}

input_file <- args[1]  # input file_name
output_file <- args[2] # output file_name

cat("输入文件:", input_file, "\n")
cat("输出文件:", output_file, "\n")


setwd("/vol/liubin/data/gwas/result")  # 运行前修改名字

library("CMplot")
library(cowplot)
pmap <- read.table(input_file, header = T)


# 阈值计算
threshold <- 0.05/0.01/nrow(pmap[!is.na(pmap$pos),])

# 标注显著基因
SNPs <- pmap[pmap[,4] < (0.000000001 / nrow(pmap)), 1]  # 测试数据添加显著性位点，无意义。实际做时仅添加目标显著位点
print(SNPs)
genes <- paste("sign_gene", 1:length(SNPs), sep="_")
print(genes)
CMplot(pmap, threshold = threshold, 
       threshold.lty=2, 
       threshold.col = "red", 
       #threshold.lty = 1, 
       amplify = F,  # 是否放大显著位点
       #points.alpha = , # 散点的透明度
       cex = c(0.5, 0.5, 0.5), 
       LOG10=TRUE,
       highlight=SNPs, # 标注目的基因
       highlight.cex=1,
       highlight.pch = 20, 
       highlight.col = "red", 
       highlight.text=genes, 
       highlight.text.col= "darkgreen", 
       pch = 19,
       band = 0.5, # the distance between chromosome
       file.output=TRUE,
       dpi = 300,
       plot.type=c("m"), 
       file = "jpg", 
       file.name = output_file)

CMplot(pmap, 
       amplify = F,
       LOG10=TRUE,
       cex = c(0.5, 0.5, 0.5), 
       file.output=TRUE,
       dpi = 300,
       plot.type=c("q"), 
       file = "jpg", 
       file.name = output_file)


