


from bert_embedding import BertEmbedding
import mxnet as mx
import numpy as np
from sentiment_analysis.utils import handle_text

class BertEmbeddingExtend(object):
    def __init__(self):
        # self.bert_embed = BertEmbedding(model='bert_12_768_12', ctx = mx.gpu(0))
        self.bert_embed = BertEmbedding(model='bert_12_768_12')

    def getSenetnceEmbedding(self, sentence, isUseAveragePooling, isUseStopwords):

        if isUseStopwords:
            new_words_list = handle_text(sentence, isUseStopwords)
            if len(new_words_list) == 0:
                 return np.zeros(768)
            sentence = " ".join(new_words_list)

        result = self.bert_embed(sentence.split('\n'))
        first_sentence = result[0]

        if first_sentence[1] == None or len(first_sentence[1]) == 0:
            return np.zeros(768)

        w_v = np.array(first_sentence[1])
        total_effect_count = w_v.shape[0]

        if isUseAveragePooling:
            w_v = np.sum(w_v, axis=0) / total_effect_count
        else:
            w_v = np.max(w_v, axis=0)

        return w_v
