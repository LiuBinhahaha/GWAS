# 获取命令行参数
# 运行前需要更改阈值，用小数或科学计数法形式

args <- commandArgs(trailingOnly = TRUE)

# 检查是否提供了必要的参数
if (length(args) != 2) {
  stop("请提供输入文件和输出文件名！\n用法: Rscript xxx.R 输入文件 输出文件")
}

input_file <- args[1]  # input file_name
output_file <- args[2] # output file_name

cat("输入文件:", input_file, "\n")
cat("输出文件:", output_file, "\n")

setwd("/data/liubin/NUE_setaria/deal_by_liubin")  # 运行前修改名字

library("CMplot")
library(cowplot)
pmap <- read.table(input_file, header = T)

# 阈值计算
#threshold <- 0.05/nrow(pmap[!is.na(pmap$pos),])

# 标注显著基因
# SNPs <- pmap[pmap[,4] < (0.000000001 / nrow(pmap)), 1]  # 测试数据添加显著性位点，无意义。实际做时仅添加目标显著位点
# print(SNPs)
# genes <- paste("sign_gene", 1:length(SNPs), sep="_")
# print(genes)

CMplot(pmap, threshold = 3.8e-5, 
       threshold.lty=2, 
       threshold.col = "red", 
       #threshold.lty = 1, 
       amplify = F,  # 是否放大显著位点
       #points.alpha = , # 散点的透明度
       cex = c(0.5, 0.5, 0.5),
       col= c("#E57373","#80CBC4","#D28FDE","#81D5F9"), 
       LOG10=TRUE,
       ylab = "-log10(P-value)",
       #highlight=SNPs, # 标注目的基因
       #highlight.cex=1,
       #highlight.pch = 20, 
       #highlight.col = "red", 
       #highlight.text=genes, 
       #highlight.text.col= "darkgreen", 
       pch = 19,
       band = 0.5, # the distance between chromosome
       file.output=TRUE,
       dpi = 600,
       plot.type=c("m","q"), 
       file = "pdf",
       file.name = output_file)

