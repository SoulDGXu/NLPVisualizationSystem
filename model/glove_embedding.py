import numpy as np
from utils import handle_text
import config


class GloveEmbedding(object):

    def __init__(self):
        '''
        初始化函数
        '''
        self.embeddings_index = {}
        self.embedding_dim_glove = 100
        self.init_data()

    def init_data(self):
        '''
        初始化数据
        :return:
        '''
        glovefile = open(config.glove_embedding_path, "r", encoding="utf-8")

        for line in glovefile:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float16')
            self.embeddings_index[word] = coefs
        glovefile.close()


    def get_embedding_matrix_glove(self, word):
        """
        获取glove词向量
        :param word:
        :return:
        """
        embedding_vector = self.embeddings_index.get(word)
        if embedding_vector is not None:
            return embedding_vector[:self.embedding_dim_glove]
        return np.zeros(self.embedding_dim_glove)

    def getSentenceVectorCommon(self, sentence, isUseAveragePooling, isUseStopwords):
        tokens = handle_text(sentence,isUseStopwords)
        total_effect_count = 0
        w_v = []
        for word in tokens:
            if word in self.embeddings_index:
                total_effect_count += 1
                w_v.append(self.embeddings_index[word])

        w_v = np.array(w_v)

        is_effect = total_effect_count > 0
        if  is_effect:
            if isUseAveragePooling:
                w_v = np.sum(w_v, axis=0) / total_effect_count
            else:
                w_v = np.max(w_v, axis=0)
        else:
            w_v = np.zeros(self.embedding_dim_glove)

        return np.array(w_v)


