#coding=utf-8
import sys
import jieba.posseg as pseg

class Find_segs(object):
    def __init__(self,words):
        self.words = words
        self.syns_of_words = []
        self.get_words_segs()


    def get_words_segs(self):
        raw_segs = pseg.cut(self.words)
        for word,tag in raw_segs:

            if 'v' in tag or 'n' in tag or 'i' in tag or 'l' in tag:
                self.syns_of_words.append(word)

        print(self.syns_of_words)

if __name__ == '__main__':

    Find_segs('英雄')
