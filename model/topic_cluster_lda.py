# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:05:43 2020

@author: Xu


基于Lda模型的多文档主题聚类,输入多篇文档,输出每个主题的关键词与相应文本,可用于主题发现与热点分析.

"""

import math
import re
import random
import numpy as np
import pandas as pd
import jieba
import config
from gensim import corpora, models,similarities


# 数据处理
def data_process(data):
    """
    Process the multiple document input: remove non-text characters, remove stop words, word segmentation, etc.,
    to generate dictionary and corpus vector.
    
    Parameters:
        data: type-list, the contents of multiple documents entered, like [doc1, doc2, ...,docn]
        
    Return:
        dictionary: type-dict, Generate dictionary based on input documents.
        corpus: type-iterator, is an iterator that returns the BOW vector
        corpus_tfidf: type-array, Calculate the TFIDF value for each feature that appears in the corpus.
        
    
    """
    # 去掉非文本字符
    
    data_new  = [re.sub(r'[^\u4e00-\u9fa5]+', '', d).strip() for d in data]
#    data_new  = [re.sub(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", '', d).strip() for d in data]
    #分词
    data_new = [list(jieba.cut(d)) for d in data_new]
    # 去停用词
    stopwords = open(config.StopWords_path,'r').read()
    stoplist = stopwords.split('\n')
    data_new = [[word for word in d if word not in stoplist] for d in data_new ]
    # 过滤长度<=1的词
    data_new = [[word for word in d if len(word)>1 ] for d in data_new ]
    #对文本进行处理，得到文本集合中的词典
    dictionary = corpora.Dictionary(data_new)
    print('number of docs: ', dictionary.num_docs)
    print('number of words: ', dictionary.num_pos)
    #利用词典，对文本进行bow表示，生成词袋
    corpus = [dictionary.doc2bow(text) for text in data_new]
    #利用bow，对文本进行tfidf表示
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return dictionary,corpus,corpus_tfidf


#  计算困惑度
def preplexity(ldamodel,testset,dictionary,size_dictionary,num_topics):
    '''
    Calculate the preplexity of a lda-model.
    Parameters:
        ldamodel: a LDA Model
        testset: corpus data
        dictionary: vocabulary, like {7822:'deferment', 1841:'circuitry',19202:'fabianism'...}
        size_dictionary: type: integer, the size of vocabulary
        num_topics: type: integer, number of tipics
    ----------
    Return:
        prep: type-float, preplexity of a lda-model
        
    '''    
    print('\n')
    print('The info of this lda-model: ')
    print('num of the testset: %s; size_dictionary: %s; num of topics: %s' %(len(testset),size_dictionary,num_topics))
    prep=0.0
    prob_doc_sum=0.0
    topic_word_list=[]  #store the prabability of topic-word
    for topic_id in range(num_topics):
        topic_word=ldamodel.show_topic(topic_id,size_dictionary)
        dic={}
        for word,probability in topic_word:
            dic[word]=probability
        topic_word_list.append(dic)
    doc_topic_list=[]  #store the doc-topic tuples:[(0, 0.0006211180124223594),(1, 0.0006211180124223594),...]
    for doc in testset:
        doc_topic_list.append(ldamodel.get_document_topics(doc,minimum_probability=0))
    testset_word_num=0
    for i in range(len(testset)):
        prob_doc=0.0     # the probability of the doc
        doc=testset[i]
        doc_word_num=0   # the number of words in the doc
        for word_id,num in doc:  #doc.items() if testset is a dic else list
            prob_word=0.0    # the probability of word
            doc_word_num+=num
            word=dictionary[word_id]
            for topic_id in range(num_topics):
                # calculate p(w): p(w)=sumz(p(z)*p(w|z))
                prob_topic=doc_topic_list[i][topic_id][1]
                prob_topic_word=topic_word_list[topic_id][word]
                prob_word+=prob_topic*prob_topic_word
            prob_doc+=math.log(prob_word)   # p(d)=sum(log(p(w)))
        prob_doc_sum+=prob_doc
        testset_word_num+=doc_word_num
    prep=math.exp(-prob_doc_sum/testset_word_num)  # perplexity=exp(-sum(p(d))/sum(Nd))
    print('the perplexity of this lda-model is: %s' %prep)
    return prep

# 确定主题个数
def get_best_num_topics(data, max_num_topics):
    """
    This is the optimal number of topics obtained through perplexity assessment.
    
    Parameters:
        data: type: array or dataframe or matrix or list, the raw text data 
        max_num_topics: type: integer, maximum of number of tipics
    
    Return:
        best_num_topics: best number of topics
       
    """
    from scipy.signal import argrelextrema
    
#    random.shuffle(data)
    train_data = data[:int(len(data)*0.6)]      
    val_data = data[int(len(data)*0.6): int(len(data)*0.8)]
    test_data = data[int(len(data)*0.8):]
       
    # 计算模型在训练和验证集上的困惑度
    preplexity_list_val=[]
    preplexity_list_train=[]

    for k in range(2, max_num_topics+1):
        dictionary,corpus,corpus_tfidf = data_process(train_data+val_data)
        ldamodel = models.LdaModel(corpus_tfidf,id2word=dictionary,num_topics=k)
        preplexity_list_train.append(preplexity(ldamodel,corpus,dictionary,len(dictionary.keys()),k))
        val_corpus = corpus[int(len(data)*0.6):]
        preplexity_list_val.append(preplexity(ldamodel,val_corpus,dictionary,len(dictionary.keys()),k))
    
    # 选择拐点（最佳主题个数）
    y1 = np.array(preplexity_list_val)
    y2 = np.array(preplexity_list_train)
    best_num_topics = argrelextrema(np.abs(y1-y2), np.less)[0][0]
    
    return  best_num_topics
    
    
# 使用lda模型，获取主题分布
def lda_model(data, file_path): 
    # data prepare 
    dictionary,corpus,corpus_tfidf = data_process(data)
    # num of topics
    num_topics = get_best_num_topics(data, 20)
    # lda model
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    # save topic keywords to the file
    output_topic_keywords = ''
    for topic in lda.print_topics(num_topics=num_topics,num_words=25):
        keywords = re.sub(r'[\d\.\d+\*]|\"','', topic[1])
        output_topic_keywords += 'Topic ' + str(topic[0]) + '\t' + keywords + '\n'
    # topic prediction/classification
    output_topic_dist = ''
    topics = lda.get_document_topics(corpus)
    topics_label = {}
    for i in range(20):
        topics_label[i] = 'Topic ' + str(i)
    # save topic distribution to the file
    for i in range(len(corpus)):
        dist = str(topics[i])
        output_topic_dist += 'Document ' + str(i+1) + '\t' + dist + '\n'
    # save     
    f = open(file_path, 'w', encoding='utf-8')
    f.write('Number of topics' + '\t' + str(num_topics) + '\n')
    f.write(output_topic_keywords)
    f.write(output_topic_dist)
    f.close()
    
    return num_topics, output_topic_keywords,  output_topic_dist  
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

