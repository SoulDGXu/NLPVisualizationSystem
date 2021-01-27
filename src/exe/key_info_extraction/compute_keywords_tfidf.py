# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:54:09 2020

@author: Xu

关键词抽取之TFIDF：
这个部分的任务是对输入文本构建词表，通过计算TF-IDF进行关键词抽取。

计算TF-IDF值：
一般有3种方法来实现：
1）用gensim库计算TFIDF值, 
from gensim import models 
tfidf = models.TfidfModel(corpus)
2）用sklearn库计算TFIDF值, 
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vec = TfidefVectorizer()
tfidf_matrix = tfidf_vec.fit_transform(corpus)
3）用python手动实现TFIDF值,
i.对语料进行分词
ii.统计词频
iii.定义计算tfidf函数
iv.计算每个单词的tfidf值

实现：
1.传入词性限制集合：调用词性标注接口，对输入句子进行词性标注，得到分词及对应的词性；
2.遍历分词结果：如果该词的词性不再词性限制集合中，则跳过；
如果词的长度小于2，或者词为停用词，则跳过；
将满足条件的词添加到词频词典中，出现的次数加1；
3.遍历词频词典，根据idf词典得到每个词的idf值，并除以词频词典中的次数总和，得到每个词的tf*idf值；
4.根据tf-idf值对词频词典中的词进行降序排序，输出topK个词作为关键词。


"""
import __init__
from src import config
from jieba import posseg


class TFIDF:
    def __init__(self):
        self.idf_file = config.idf_path
        self.idf_dict, self.common_idf = self.load_idf()
        
    def load_idf(self):
        idf_dict = {}
        for line in open(self.idf_file, 'r', encoding='utf-8').readlines():
            try:
                word, freq = line.strip().split(' ')
            except:
                word, freq = line.strip().split('\t')
            idf_dict[word] = float(freq)
        common_idf = sum(idf_dict.values())/len(idf_dict)

        return idf_dict, common_idf
    

    def build_wordsdict(self, text):
        word_dict = {}
        candi_words = []
        candi_dict = {}
        for word in posseg.cut(text):
            if word.flag[0] in ['n', 'v', 'a'] and len(word.word) > 1:
                candi_words.append(word.word)
            if word.word not in word_dict:
                word_dict[word.word] = 1
            else:
                word_dict[word.word] += 1
        count_total = sum(word_dict.values())
        for word, word_count in word_dict.items():
            if word in candi_words:
                candi_dict[word] = word_count/count_total
            else:
                continue

        return candi_dict

    def extract_keywords(self, text, num_keywords):
        keywords_dict = {}
        candi_dict = self.build_wordsdict(text)
        for word, word_tf in candi_dict.items():
            word_idf = self.idf_dict.get(word, self.common_idf)
            word_tfidf = word_idf * word_tf
            keywords_dict[word] = word_tfidf
        keywords_dict = sorted(keywords_dict.items(), key=lambda asd:asd[1], reverse=True)

        return keywords_dict[:num_keywords]

    










































