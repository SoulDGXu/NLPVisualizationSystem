# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:06:16 2020

@author: Xu
"""
import __init__
from gensim import models
from src import config
import numpy as np

# import os
# import sys 
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.append(os.path.split(rootPath)[0])


class SimilarityCompute:
    def __init__(self):
        self.embedding_file = config.token_vector_path
        self.model = models.KeyedVectors.load_word2vec_format(self.embedding_file, binary=False)

    def get_wordvector(self, word):
        try:
            return self.model[word]
        except:
            return np.zeros(200)

    def similarity_cosine(self, word_list1,word_list2):
        simalrity = 0
        vector1 = np.zeros(200)
        for word in word_list1:
            vector1 += self.get_wordvector(word)

        vector1 = vector1/len(word_list1)
        vector2 = np.zeros(200)

        for word in word_list2:
            vector2 += self.get_wordvector(word)

        vector2 = vector2/len(word_list2)
        cos1 = np.sum(vector1*vector2)
        cos21 = np.sqrt(sum(vector1**2))
        cos22 = np.sqrt(sum(vector2**2))
        similarity = cos1/float(cos21*cos22)
        return similarity
