# -*- encoding: utf-8 -*-
'''
@File    :   tried_dar.py
@Time    :   2020/08/12 10:49:15
@Author  :   huangdingbang@baidu.com
@Desc    :   基于双数组，实现Tried树
'''

from collections import Counter
import numpy as np


def get_children(words, begin, end, prefix):
    length = len(prefix)
    children = []
    for i, word in enumerate(words[begin:end]):
        if len(word) == length:
            children.append(("", i + begin, -1))
        elif not children or word[length] != children[-1][0]:
            children.append((word[length], i + begin, ord(word[length])))

    return children


class TriedTree(object):
    """docstring for Darts"""

    def __init__(self, init_size=100):
        super(TriedTree, self).__init__()
        self.base = [0] * init_size
        self.check = [-1] * init_size
        self.use = [False] * init_size
        self.words = []

        self.min_free = 1
        self.offset = 0
        self.base[0] = 1
        self.check[0] = 0

    def __expend__(self, size):
        self.base += [0] * size
        self.check += [-1] * size
        self.use += [False] * size

    def set_offset(self, words):
        self.offset = 2000000
        for word in words:
            for char in word:
                self.offset = min(self.offset, ord(char))
        self.offset = - self.offset + 1

    def add_word(self, word):
        self.words.append(word)

    def get_base(self, start, children):
        i = 0
        for char, offset, code in children:
            if code == -1:
                i += 1
                continue
            break
        else:
            return start

        while self.use[start]:
            start += 1

        while True:
            for char, offset, code in children[i:]:
                try:
                    if self.check[start + code] != -1:
                        start += 1
                        break
                except:
                    # 越界except，扩展空间[新空间必为-1]
                    while start + code >= len(self.check):
                        self.__expend__(len(self.check))
                    continue
            else:
                break

        self.use[start] = True

        return start


    def get_state(self, state, char):

        next_state = abs(self.base[state]) + ord(char)
        if next_state > len(self.base) or self.check[next_state] != state:
            return -1
        else:
            return next_state

    def make(self):
        self.words.sort()

        queue = list()
        queue.append((0, len(self.words), "", 0))

        while queue:
            begin, end, prefix, cur_state = queue.pop(0)

            children = get_children(self.words, begin, end, prefix)

            start = cur_state + 1

            start = self.get_base(start, children)

            self.base[cur_state] = start

            for i, (char, offset, code) in enumerate(children):
                if not char:
                    self.base[cur_state] = - start
                    continue

                next_state = abs(self.base[cur_state]) + code
                self.check[next_state] = cur_state

                if i == len(children) - 1:
                    queue.append((offset, end, prefix + char, next_state))
                    continue
                queue.append(
                    (offset, children[i + 1][1], prefix + char, next_state))

    def search(self, query):
        res = []
        for i, char in enumerate(query):
            cur_state = 0
            j = 0
            while True:
                if i + j == len(query):
                    break
                cur_state = self.get_state(cur_state, query[i + j])
                if cur_state < 0:
                    break

                j += 1
                if self.base[cur_state] < 0:
                    res.append(query[i: i + j])
        return res



if __name__ == '__main__':
    x = ["百度", "家", "家家", "高科技", "技公", "科技", "科技公司"]
    darts = TriedTree(20000)
    for word in x:
        darts.add_word(word)
    darts.make()
    string = '百度是家高科技公司'
    print(darts.search(string))



