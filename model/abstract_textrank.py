# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:08:56 2020

@author: Xu
"""

from collections import defaultdict
import jieba.posseg as pseg
from textrank import *
from sentence_similarity import *
import re
from create_wordcloud import *

class AbstarctTextrank:
    def __init__(self):
        self.span = 3
        self.similer = SimilarityCompute()
        self.sim_score = 0.5 #句子相似度阈值，用于构建句子之间的边

    def sentence_split(self, text):
        sentence_dict = {}
        sentences = [sentence.strip() for sentence in re.split(r'[？！。;；\n\r]', text) if sentence]
        for index, sentence in enumerate(sentences):
            sentence_dict[index] = [sentence, [word.word for word in pseg.cut(sentence) if word.flag[0] not in ['x', 'u', 'p', 'w']]]
        return sentence_dict

    def extract_abstract(self, text, num_sentences):
        sentence_dict = self.sentence_split(text)
        g = textrank_graph()
        cm = defaultdict(int)
        for i, s1 in sentence_dict.items():
            for j, s2 in sentence_dict.items():
                sim_score = self.similer.similarity_cosine(s1[1], s2[1])
                if sim_score >= 0.5:
                    cm[(s1[0], s2[0])] += 1
        for terms, w in cm.items():
            g.addEdge(terms[0], terms[1], w)
        nodes_rank = g.rank()
        nodes_rank = sorted(nodes_rank.items(), key=lambda asd: asd[1], reverse=True)
        return nodes_rank[:num_sentences]






