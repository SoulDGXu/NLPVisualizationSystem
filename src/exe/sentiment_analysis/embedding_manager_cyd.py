from sentiment_analysis.glove_embedding import GloveEmbedding
from  sentiment_analysis.bert_embedding_extend import BertEmbeddingExtend
from enum import Enum

class Embedding_Type(Enum):
    glove = 0,
    bert = 1

class EmbeddingManagerCyd(object):
    def __init__(self):
        self.gloveEmbedding = GloveEmbedding()
        self.bertEmbedding = BertEmbeddingExtend()

    def getEmbedding(self, sentence, type, isUseAveragePooling, isUseStopwords):
        if type == Embedding_Type.glove:
            return self.gloveEmbedding.getSentenceVectorCommon(sentence, isUseAveragePooling, isUseStopwords)
        elif type == Embedding_Type.bert:
            return self.bertEmbedding.getSenetnceEmbedding(sentence, isUseAveragePooling, isUseStopwords)

        return None
