# -*- coding: utf-8 -*-
""" Construct A Trie Tree for Searching

Provide a class interface to
boost the process of searching strings.

Author: Li Dongsheng
Project:https://github.com/ldsyou92/algorithm-per-week/new/master
Created on 2019/03/10
"""

import time

class Trie:
    # word_end = -1

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = {}
        self.word_end = -1

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        curNode = self.root
        for c in word:
            if not c in curNode:
                curNode[c] = {}
            curNode = curNode[c]

        curNode[self.word_end] = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        curNode = self.root
        for c in word:
            if not c in curNode:
                return False
            curNode = curNode[c]

        # Doesn't end here
        if self.word_end not in curNode:
            return False

        return True

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        curNode = self.root
        for c in prefix:
            if not c in curNode:
                return False
            curNode = curNode[c]

        return True

def main():
    # Your Trie object will be instantiated and called as such:
    obj = Trie()
    begin = time.time()
    obj.insert('荣盛的bu可能'.strip())
    new_word = '荣盛的bu可能'
    if not obj.search(new_word):
        print "title not found"
    else:
        print "woho"
    end = time.time()
    print end-begin
    print obj.search('降了！大势所趋！苏州多家银行利率回调！')

if __name__ == '__main__':
    main()
