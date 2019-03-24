# coding:utf-8
"""
二分K-means算法
"""
import numpy as np
import random
import math
import matplotlib.pyplot as plt


def readText(inputfile):
    lines = open(inputfile, "r").readlines()
    dataSet = []
    for line in lines:
        dataList = line.strip().split(',')
        dataSet.append([float(dataList[1]), float(dataList[2])])
    return dataSet


def transDataSet(dataSet):
    hang, lie = dataSet.shape
    new_data = np.zeros((hang, lie))
    for i in range(hang):
        new_data[i, :] = dataSet[i, :]
    return new_data


def initClusterpoints(dataSet, k):
    hang, lie = dataSet.shape
    clusterPoints = np.zeros((k, lie))
    for i in range(k):
        index = int(random.uniform(0, hang))
        clusterPoints[i, :] = dataSet[index, :]
    return clusterPoints


def calDis(v1, v2):
    s = (sum(pow(v1 - v2, 2)))
    return s


def calSSE(dataSubset, cleaterPoint):
    dataSubset = transDataSet(dataSubset)
    cleaterPoint = transDataSet(cleaterPoint)
    dataSubset_hang = dataSubset.shape[0]
    sum_dis = 0
    for i in range(dataSubset_hang):
        sum_dis = sum_dis + calDis(dataSubset[i, :], cleaterPoint[0, :])
    return sum_dis


def bisKmeans(dataSet, k):
    # 将初始的一个cluster一分为二
    hang, lie = dataSet.shape
    # clusterCenter = np.zeros((k,lie))
    clusterAssment = np.zeros((hang, lie))
    for i in range(hang):
        clusterAssment[i, 0] = 0
    currentClusterPoints = np.mean(dataSet, axis=0).tolist()[0]
    cenList = {0: [currentClusterPoints]}
    clusterNum = 1

    while clusterNum < k:
        maxSSE = 0.00001
        maxSSEIndex = 0.0
        for j in range(clusterNum):  # 得到最大的SSE
            currentDataSet = dataSet[np.nonzero(clusterAssment[:, 0] == j)[0]]
            currentSSE = calSSE(currentDataSet, np.mat(cenList[j]))

            if currentSSE >= maxSSE:
                maxSSE = currentSSE
                maxSSEIndex = j

        currentDataSet = dataSet[np.nonzero(clusterAssment[:, 0] == maxSSEIndex)[0]]
        currentClusterPoints, currentClusterAssment = Kmeans(currentDataSet, 2)

        if clusterNum == 1:
            clusterAssment = currentClusterAssment

        else:
            # 把新分出来的两部分分别打上标签。
            currentClusterAssment[np.nonzero(currentClusterAssment[:, 0] == 1)[0], 0] = clusterNum
            currentClusterAssment[np.nonzero(currentClusterAssment[:, 0] == 0)[0], 0] = maxSSEIndex

            clusterAssment[np.nonzero(clusterAssment[:, 0] == maxSSEIndex)[0], :] = currentClusterAssment

        # 更新聚类中心
        cenList[clusterNum] = currentClusterPoints[1, :]
        cenList[maxSSEIndex] = currentClusterPoints[0, :]

        clusterNum += 1

    return cenList, clusterAssment


def Kmeans(dataSet, k):
    clusterPoints = initClusterpoints(dataSet, k)
    new_dataSet = transDataSet(dataSet)
    hang, lie = dataSet.shape
    clusterAssment = np.zeros((hang, lie))
    clusterChanged = True

    while clusterChanged:
        clusterChanged = False
        # 计算每个点与各个中心点的距离
        for i in range(hang):
            min_dis = 10000.0
            min_index = 0
            for j in range(k):
                distance = calDis(new_dataSet[i, :], clusterPoints[j, :])
                if distance < min_dis:
                    min_dis = distance
                    min_index = j
            # 将每个点归类
            if clusterAssment[i, 0] != min_index:
                clusterChanged = True
                clusterAssment[i, 0] = min_index
        # 更新聚类中心
        for j in range(k):
            points = dataSet[np.nonzero(clusterAssment[:, 0] == j)[0]]
            clusterPoints[j, :] = np.mean(points, axis=0)
    # print(u"聚类成功！")
    return clusterPoints, clusterAssment


def showCluster(dataSet, k, centroids, clusterAssment):
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    numSamples, dim = dataSet.shape
    plt.title(u"The results of k=%d" % k)
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("Sorry! Your k is too large! please contact Zouxy")
        return 1

    # draw all samples
    for i in range(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])  # 把所有点先画出来，根据聚类结果来标记不同分类的点。

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):  # 画出聚类中心
        plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize=12)
    plt.show()


if __name__ == "__main__":
    inputfile = r"../k-means20190317/testSet.txt"
    dataSet = np.mat(readText(inputfile))
    a, b = bisKmeans(dataSet, 4)
    # a, b = Kmeans(dataSet, 4)
    showCluster(dataSet, 4, a, b)