# coding=utf-8
"""
k-means聚类算法
"""

from numpy import *


def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        # 将每一行的数据映射成float型
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat


# 计算两个向量的距离，用的是欧几里得距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


# 随机生成初始的质心（ng的课说的初始方式是随机选K个点）
def randCent(dataSet, k):
    # 计算样本的维度
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))
    # 遍历数据的每一维度
    for j in range(n):
        # 计算该列的最小值
        minJ = min(dataSet[:, j])
        # 计算该列的最大值与最小值的差
        rangeJ = float(max(array(dataSet)[:, j]) - minJ)
        # 随机生成k个质心的位置
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    # 获得样本数量
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    # 创建k个质心的向量
    centroids = createCent(dataSet, k)
    # clusterChanged表示聚类结果是否发生变化
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                # 计算数据点到质心的距离
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI;
                    minIndex = j
            # 如果第i个样本的聚类结果发生变化：布尔类型置为true，继续聚类算法
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2
        print centroids
        for cent in range(k):
            # 将数据集中所有属于当前质心类的样本通过条件过滤筛选出来
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            # 计算每一列的均值作为这一类的质心向量
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


def show(dataSet, k, centroids, clusterAssment):
    from matplotlib import pyplot as plt
    numSamples, dim = dataSet.shape
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    for i in xrange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)
    plt.show()


def main():
    dataMat = mat(loadDataSet('testSet.txt'))
    myCentroids, clustAssing = kMeans(dataMat, 4)
    print myCentroids
    show(dataMat, 4, myCentroids, clustAssing)


if __name__ == '__main__':
    main()