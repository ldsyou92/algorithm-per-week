#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
对字符串去停用词后分词，
按fasttext的格式打标签
格式为:"__label__<label_name> <text>"
Created by lidongsheng on 2019/04/25
"""
import jieba
from delete_html import FilterTag

def process_input():
    filters = FilterTag()
    # 相关性小标记为1，过审的为0
    fw = open('val_001.txt', 'w')
    with open('article_2weeks_001.txt', 'r') as f:
        input = f.readlines()
    for each in input:
        article = filters.filterHtmlTag(each)
        line = seg_sentence(article)
        #print(line)
        fw.write("__label__001\t"+line + "\n")
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
