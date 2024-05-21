setwd("/vol/liubin/data/gwas")
library("CMplot")
pmap <- read.table("show_test.pmap", header = T)
head(pmap)

# 阈值计算
threshold <- 1/nrow(pmap[!is.na(pmap$pos),])
# 画图
CMplot(pmap, threshold = threshold, amplify = F, file = "tiff", plot.type=c("m","q"))

plot.type="m"：曼哈顿图
plot.type：可以选择 "d", "c", "m", "q" or "b"
plot.type="d", SNP密度图
plot.type="c", 环形曼哈顿图
plot.type="m",曼哈顿图
plot.type="q",QQ图
plot.type="b",同时绘制环形曼哈顿图、曼哈顿图和QQ图
plot.type=c("m","q"), 绘制曼哈顿图和QQ图
