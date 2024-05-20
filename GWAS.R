setwd("/vol/liubin/data/gwas")
library("CMplot")
pmap <- read.table("show_test.pmap", header = T)
head(pmap)

# 阈值计算
threshold <- 1/nrow(pmap[!is.na(pmap$pos),])
# 画图
CMplot(pmap, threshold = threshold, amplify = F, file = "tiff", plot.type=c("m","q"))
