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
    fw = open('test_0.txt', 'w')
    with open('100') as f:
        input = f.readlines()
    for each in input:
        print (each)
        article = filters.filterHtmlTag(each)
        line = list(jieba.cut(article))
        sentence =  "\t".join(line)
        fw.write("0\t"+sentence)

    fw.close()

def main():
    process_input()

if __name__ == '__main__':
    main()
