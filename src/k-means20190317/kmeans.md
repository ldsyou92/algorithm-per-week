#K-means算法
聚类是一种无监督的学习，它将相似的对象归到同一簇中。聚类的方法几乎可以应用所有对象，簇内的对象越相似，聚类的效果就越好。K-means算法中的k表示的是聚类为k个簇，means代表取每一个聚类中数据值的均值作为该簇的中心，或者称为质心，即用每一个的类的质心对该簇进行描述。

聚类分析试图将相似的对象归入同一簇，将不相似的对象归为不同簇，那么，显然需要一种合适的相似度计算方法，我们已知的有很多相似度的计算方法，比如欧氏距离，余弦距离，汉明距离等。事实上，我们应该根据具体的应用来选取合适的相似度计算方法。

##优点：
容易实现
##缺点：
可能收敛到局部最小值，在大规模数据集上收敛较慢

#在最后
之所以要看一下这个，是因为yolo里面anchor会有一个预设值，是用k-means聚类得到的，所以在分析那个之前，先把k-means重新看了一下，遇到的问题是感觉yolo的那个计算不准，想改进一下，希望下周能实现。