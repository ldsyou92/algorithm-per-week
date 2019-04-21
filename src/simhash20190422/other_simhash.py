#coding:utf8
import math
import jieba
import jieba.analyse

class SimHash(object):

    def __init__(self):
        pass

    def getBinStr(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            # print(source, x)

            return str(x)


    def getWeight(self, source):
        # fake weight with keyword
        return ord(source)
    def unwrap_weight(self, arr):
        ret = ""
        for item in arr:
            tmp = 0
            if int(item) > 0:
                tmp = 1
            ret += str(tmp)
        return ret

    def simHash(self, rawstr):
        seg = jieba.cut(rawstr, cut_all=True)
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=100, withWeight=True)
        print(keywords)
        ret = []
        for keyword, weight in keywords:
            binstr = self.getBinStr(keyword)
            keylist = []
            for c in binstr:
                weight = math.ceil(weight)
                if c == "1":
                    keylist.append(int(weight))
                else:
                    keylist.append(-int(weight))
            ret.append(keylist)
        # 对列表进行"降维"
        rows = len(ret)
        if rows:
            cols = len(ret[0])
        else:
            cols = 0
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)

    def getDistince(self, hashstr1, hashstr2):
        length = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:
                continue
            else:
                length += 1
        return length


if __name__ == "__main__":
    simhash = SimHash()
    s1 = "在Python中，通过内置的re模块提供对正则表达式的支持。正则表达式会被编译成一系列的字节码，然后由通过C编写的正则表达式引擎进行执行。该引擎自从Python1.6被内置以来，近20年时间未有发生过变化，实乃我辈楷模。吴亦凡的新歌大碗宽面简直不要太好听，如果他还出专辑，我一定第一个去买"
    s2 = "在Python中，通过内置的re模块提供对正则表达式的支持。正则表达式会被编译成一系列的字节码，然后由通过C编写的正则表达式引擎进行执行。该引擎自从Python1.6被内置以来，近20年时间未有发生过变化，实乃我辈楷模。蔡徐坤的新歌大碗宽面简直不要太好听，如果他还出专辑，我一定第一个买"
    #with open("a.txt", "r") as file:
    #    s1 = "".join(file.readlines())
    #    file.close()
    #with open("b.txt", "r") as file:
    #    s2 = "".join(file.readlines())
    #    file.close()
    # s1 = "this is just test for simhash, here is the difference"
    # s2 = "this is a test for simhash, here is the difference"
    print(simhash.getBinStr(s1))
    print(simhash.getBinStr(s2))
    hash1 = simhash.simHash(s1)
    hash2 = simhash.simHash(s2)
    distince = simhash.getDistince(hash1, hash2)
    # value = math.sqrt(len(s1)**2 + len(s2)**2)
    value = 5
    print("海明距离：", distince, "判定距离：", value, "是否相似：", distince<=value)

