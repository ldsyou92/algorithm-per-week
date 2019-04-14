#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
处理数据，去掉html标签并对数据进行标注
Created by lidongsheng on 2019/03/31
"""
import jieba
from delete_html import FilterTag

def process_input():
    filters = FilterTag()
    # 相关性小标记为1，过审的为0
    fw = open('train_1.txt', 'w')
    with open('与平台内容相关性小.tsv', 'r') as f:
        input = f.readlines()
    for each in input:
        article = filters.filterHtmlTag(each)
        line = seg_sentence(article)
        print(line)
        fw.write("1\t"+line + "\n")

    fw.close()


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords


# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip(), cut_all=False)
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


def main():
    process_input()


if __name__ == '__main__':
    main()
