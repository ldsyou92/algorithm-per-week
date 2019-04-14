# coding=UTF-8
from numpy import *
import matplotlib.pyplot as plt
import time
import math
import re


def loadTrainDataSet():  # 读取训练集
    fileIn = open('train.txt')
    postingList = []  # 邮件表，二维数组
    classVec = []
    i = 0
    for line in fileIn.readlines():
        lineArr = line.strip().split()
        temp = []
        for i in range(len(lineArr)):
            if i == 0:
                classVec.append(int(lineArr[i]))
            else:
                temp.append(lineArr[i])
        postingList.append(temp)
        i = i + 1
        print(i)
    return postingList, classVec


def createVocabList(dataSet):  # 创建词典
    vocabSet = set([])  # 定义list型的集合
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):  # 对于每一个训练样本，得到其特征向量
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            pass
            # print("\'%s\' 不存在于词典中"%word)
    return returnVec


def createTrainMatrix(vocabList, postingList):  # 生成训练矩阵，即每个样本的特征向量
    trainMatrix = []  # 训练矩阵
    for i in range(len(postingList)):
        curVec = setOfWords2Vec(vocabList, postingList[i])
        trainMatrix.append(curVec)
    return trainMatrix


def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)  # 样本数量
    print(numTrainDocs)
    numWords = len(trainMatrix[0])  # 样本特征数
    print(numWords)
    pAbusive = sum(trainCategory) / float(numTrainDocs)  # p(y=1)
    # 分子赋值为1，分母赋值为2（拉普拉斯平滑）
    p0Num = ones(numWords);  # 初始化向量，代表所有0类样本中词j出现次数
    p1Num = ones(numWords);  # 初始化向量，代表所有1类样本中词j出现次数
    p0Denom = p1Denom = 2.0  # 代表0类1类样本的总词数
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num / p1Denom  # 概率向量(p(x0=1|y=1),p(x1=1|y=1),...p(xn=1|y=1))
    p0Vect = p0Num / p0Denom  # 概率向量(p(x0=1|y=0),p(x1=1|y=0),...p(xn=1|y=0))
    # 取对数，之后的乘法就可以改为加法，防止数值下溢损失精度
    p1Vect = log(p1Vect)
    p0Vect = log(p0Vect)
    return p0Vect, p1Vect, pAbusive


def classifyNB(vocabList, testEntry, p0Vec, p1Vec, pClass1):  # 朴素贝叶斯分类
    # 先将输入文本处理成特征向量
    # regEx = re.compile('\\W*')  # 正则匹配分割，以字母数字的任何字符为分隔符
    #testArr = regEx.split(testEntry)
    testArr = testEntry
    print(testArr)
    testVec = array(setOfWords2Vec(vocabList, testArr))
    # 此处的乘法并非矩阵乘法，而是矩阵相同位置的2个数分别相乘
    # 矩阵乘法应当 dot(A,B) 或者 A.dot(B)
    # 下式子是原式子取对数，因此原本的连乘变为连加
    p1 = sum(testVec * p1Vec) + log(pClass1)
    p0 = sum(testVec * p0Vec) + log(1.0 - pClass1)
    # 比较大小即可
    if p1 > p0:
        return 1
    else:
        return 0


# 测试方法
def testingNB():
    begin = time.time()
    postingList, classVec = loadTrainDataSet()
    vocabList = createVocabList(postingList)
    trainMatrix = createTrainMatrix(vocabList, postingList)
    p0V, p1V, pAb = trainNB0(trainMatrix, classVec)
    # 输入测试文本，单词必须用空格分开
    # testEntry = """
    # 哈尔滨	大盛	地产	经纪人	许超	，	入职	三个	月	以来	，	还	没有	成交	一单	。	当	感觉	自己	不	适合	这个	工作	想要	转行	的	时候	，	一次	社区活动	，	竟	意外	地	让	他	在	三天	内	便	卖出	了	一	套房	......	哈尔滨	大盛	地产	厅	振兴	店	经纪人	许超入	职	以来	第一	单	2019	年	3	月	16	日	这	一天	，	贝壳	找房	一场	市场推广	的	社区活动	，	在	哈尔滨	居然	之	家	举办	。	经过	精心策划	，	此次	活动	借势	热门	综艺	《	妻子	的	浪漫	旅行	》	第二季	，	组织	经纪人	进行	好房	推荐	，	其中	还有	拍照	框	、	VR	看房	、	奖品	等	免费	福利	，	这些	新颖	的	物件	儿	极富	吸引力	，	不一会儿	商场	里	就	聚集	了	很多	人	。	贝壳	找房	活动	现场	而	经纪人	许超	碰巧	被	分配	在	了	这次	活动	，	负责	为	来往	的	客户	讲解	推介	房源	。	此前	，	许超	几乎	没	参加	过	类似	的	社区	互动	，	“	当时	还	有些	紧张	的	，	在	现场	就是	要	找到	一些	可能	感兴趣	的	顾客	。	”	据	许超	回忆	，	当时	一位	五十多岁	、	背着	小包	的	阿姨	对	展览	看来看去	，	还	拿出	手机	不断	拍照	。	许超	走上	前	询问	：	“	这位	阿姨	，	您	是	想	看看	咱	的	新	房源	吗	？	”	“	我	就	随便	看看	，	小伙子	，	这	贝壳	找房	的	软件	怎么弄	啊	我	不太会	。	”	“	来	，	我来	教	您	…	…	”	起初	，	阿姨	没有	提出	明确	的	带	看房	邀约	，	许超	也	以为	她	是	图个	热闹	。	但是	，	仍	十分	热情	地	满足	她	的	需求	。	帮	阿姨	注册	账号	，	并	教会	阿姨	如何	使用	VR	看房	。	最后	，	阿姨	留下	了	许超	的	电话号码	。	经纪人	为	市民	讲解	房源	让	他	没想到	的	是	，	第二天	晚上	，	电话铃	声响	了	，	竟然	就是	昨天	社区活动	遇到	的	那个	阿姨	，	和	许超聊	了	两天	后	，	她	利用	VR	看房	很快	筛选	到	了	想	看	的	房子	，	省去	了	四处	周折	的	麻烦	。	几经考虑	后	，	阿姨	想要	许超带	着实	地	看房	。	18	号	早上	6	点	10	分	，	哈尔滨	风	很大	、	气温	骤降	，	昏黄	的	街灯	下	，	许超	拿	着	几套	房源	的	钥匙	，	带	着	阿姨	开始	了	看房	。	原来	，	这位	阿姨	是	附近	县城	的	，	女儿	在	哈尔滨	工作	，	她	也	想	把	家	搬	到	城市	里	。	从	县城	赶来	看房	刚好	碰上	贝壳	找房	的	这次	活动	，	对	买房	不	了解	的	她	，	被	许超	的	热情	和	真诚	打动	。	截止	下午	两点	，	两个	人	就	一起	看	了	三四	套	房子	了	。	最终	，	她	看中	了	一套	五六十	平	的	两居室	，	并	要求	尽快	签约	。	从	上午	6	点到	现在	也	不过	8	小时	，	一套	房子	就	这样	顺利	地	成交	了	。	阿姨	的	亲戚	也	在	同时	帮	她	看房	，	但	最后	她	为什么	选择	了	许超	，	阿姨	只	说	了	一句	话	：	“	这个	小伙子	贼	靠	谱	，	我	和	他	看	了	几	套房	。	房子	好	就是	好	，	不好	他	也	会	说	。	”	是	啊	，	真诚	，	是	一个	经纪人	最	可贵	的	品质	。	“	我	现在	卖	的	是	什么	？	是	服务	，	不是	别的	。	”	许超	这样	形容	自己	的	职业	第一	单	，	他	并	不	觉得	这	是	多	大	的	成就	，	只是	觉得	这是	应该	做	的	事情	。	这是	许超入	职	以来	的	第一	单	，	意料之外	，	也	在	意料之中	。	与其	坐	门店	，	不如	进社区	正	如许	超	所说	：	“	与其	坐在	门店	没事干	，	还	不如	进社区	。	”	很多	时候	，	经纪人	没有	带	看	任务	时	，	出去	获客	成为	了	必要	的	日程	。	 	由	贝壳	找房	平台	联动	各大	品牌	商	发起	进社区	活动	，	在	和	大家	打交道	的	过程	中	，	方便	市民	了解	购房	信息	，	将	服务	送到	身边	，	也	增加	了	经纪人	和	大家	的	联系	。	<	img
    # """
    # testEntry='fuck you bitch!!!'
    # print(classifyNB(vocabList, testEntry, p0V, p1V, pAb))
    tr = 0
    wr = 0
    with open('test_0.txt', 'r') as f:
        for line in f:
            testEntry = line
            # print('测试文本为： ' + testEntry)
            if classifyNB(vocabList, testEntry, p0V, p1V, pAb):
                tr += 1
                print("--------与平台相关性小--------")
            else:
                wr += 1
                print("--------正常文章--------")
            end = time.time()
    print(tr)
    print(wr)
    print("运行时间为：{}s".format(end-begin))


if __name__ == '__main__':
    testingNB()
