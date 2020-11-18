# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 22:39:56 2020

@author: Xu

对于中国临床试验注册中心(ChiCTR)的注册项目的主题分析：
了解目前注册项目库中最具代表性的研究主题，计算每个研究项目对应哪些主题。

基于Lda模型的多文档主题聚类,输入多篇文档,输出每个主题的关键词与相应文本,可用于主题发现与热点分析.



"""
import math
import re
import random
import pandas as pd
import jieba
from gensim import corpora, models,similarities


# ######################################################################################
# ======================================================================================
#                            利用sklearn构建LDA中文主题模型
# ======================================================================================

## 1. laod data
data_path = './data/self_info_results_all.xls'
df = pd.read_excel(data_path)
trails = df['注册题目'].values.tolist()

## 2. 预处理
# 分词
corpus = []
for trail in trails:
    doc_cut = jieba.cut(trail, cut_all=False)
    result = ' '.join(doc_cut)
    corpus.append(result)
    
# 去停用词
stpwrdpath = "stop_words_ch.txt"
stpwrd_dic = open(stpwrdpath, 'rb')
stpwrd_content = stpwrd_dic.read() 
stpwrdlst = stpwrd_content.splitlines()
stpwrd_dic.close()

# tfidf特征处理
from sklearn.feature_extraction.text import CountVectorizer

cntVector = CountVectorizer(stop_words=stpwrdlst)
cntTf = cntVector.fit_transform(corpus)
print( cntTf)
wordlist = cntVector.get_feature_names()#获取词袋模型中的所有词   
weightlist = cntTf.toarray()     
   

## 3. 构建主题模型
# LDA是基于词频统计的
from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_topics=2,
                                learning_offset=50.,
                                random_state=0)
# 得到文档的主题模型分布
trail_res = lda.fit_transform(cntTf)
print('文档主题的分布: \n',trail_res)
print('主题和词的分布: \n', lda.components_)
print('困惑度perplexity: ', lda.perplexity(cntTf))
print('对数似然得分: ', lda.score(cntTf))


# #######################################################################################
# ======================================================================================
#                            确定主题个数
# ======================================================================================

## LDA 主题模型中主题个数的确定
def preplexity(ldamodel,testset,dictionary,size_dictionary,num_topics):
    '''calculate the preplexity of a lda-model'''
    # dictionary : {7822:'deferment', 1841:'circuitry',19202:'fabianism'...]
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

def data_process(data):
    data_new = []
    # 去掉非文本字符
    for line in data:
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "",line)
        data_new.append(line.strip())
    #分词
    data_set = []
    for d in data_new:
        wordlist = list(jieba.cut(d, cut_all=False))
        data_set.append(wordlist)
    # 去停用词
    stopwords = pd.read_csv("stop_words_ch.txt",index_col=False,quoting=3,sep=" ",names=['stopword'],encoding='gb18030')
    stpwrdlst = stopwords['stopword'].values.tolist()
    data_remove_stpwrd = []
    for d in data_set:
        d_new = []
        for word in d:
            if word not in stpwrdlst:
                d_new.append(word)
        data_remove_stpwrd.append(d_new)           
    data_set = data_remove_stpwrd
    #对文本进行处理，得到文本集合中的词表
    dictionary = corpora.Dictionary(data_set)
    #利用词表，对文本进行bow表示
    corpus = [dictionary.doc2bow(text) for text in data_set]
    #利用bow，对文本进行tfidf表示
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return dictionary,corpus,corpus_tfidf

# 将样本划分为训练集、验证集、测试集：各占6：2：2
data_path = 'D:/MS/项目经验/2爬虫/Python爬取ChiCTR数据/data/self_info_results_all.xls'
df = pd.read_excel(data_path)
data = df['注册题目'].values.tolist()
random.shuffle(data)
train_data = data[:int(len(data)*0.6)] 
val_data = data[int(len(data)*0.6): int(len(data)*0.8)]
test_data = data[int(len(data)*0.8):]

# 计算模型在训练和验证集上的困惑度
preplexity_list_val=[]
preplexity_list_train=[]

for k in range(2,20):
    dictionary,corpus,corpus_tfidf = data_process(train_data+val_data)
    ldamodel = models.LdaModel(corpus_tfidf,id2word=dictionary,num_topics=k)
    preplexity_list_train.append(preplexity(ldamodel,corpus,dictionary,len(dictionary.keys()),k))
    val_corpus = corpus[int(len(data)*0.6):]
    preplexity_list_val.append(preplexity(ldamodel,val_corpus,dictionary,len(dictionary.keys()),k))
    
    
# 模型在训练和验证集上的困惑度曲线
import matplotlib.pyplot as plt

fig=plt.figure()
K = list(range(2,20))
plt.plot(K,preplexity_list_val,'bo-',label='Validation')
plt.plot(K,preplexity_list_train,'ro-',label='Training')
plt.legend()
plt.xlabel('num_topics')
plt.ylabel('preplexity')
plt.show()


# 模型在测试集上的效果
best_num_topics = 6
best_ldamodel = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=best_num_topics)
test_dictionary,test_corpus,test_corpus_tfidf = data_process(test_data)
topics_test = best_ldamodel.get_document_topics(test_corpus)
for i in range(len(test_corpus)):
    print('[{}] Topic distribution: {}\n'.format(i, topics_test[i]))

# ########################################################################################
# ======================================================================================
#                     利用gensim构建LDA模型:基于LDA的临床医学主题词分布研究
# ======================================================================================
   
# 构建数据，先后使用doc2bow和tfidf model对文本进行向量表示
def create_data(corpus_path):
    df = pd.read_excel(corpus_path)
    data = df['注册题目'].values.tolist()
    data_new = []
    # 去掉非文本字符
    for line in data:
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "",line)
        data_new.append(line.strip())
    #分词
    train_set = []
    for d in data_new:
        wordlist = list(jieba.cut(d, cut_all=False))
        train_set.append(wordlist)
    # 去停用词
    stopwords = pd.read_csv("stop_words_ch.txt",index_col=False,quoting=3,sep=" ",names=['stopword'],encoding='gb18030')
    stpwrdlst = stopwords['stopword'].values.tolist()
    train_remove_stpwrd = []
    for train in train_set:
        train_new = []
        for word in train:
            if word not in stpwrdlst:
                train_new.append(word)
        train_remove_stpwrd.append(train_new)           
    train_set = train_remove_stpwrd
    #对文本进行处理，得到文本集合中的词表
    dictionary = corpora.Dictionary(train_set)
    #利用词表，对文本进行bow表示
    corpus = [dictionary.doc2bow(text) for text in train_set]
    #利用bow，对文本进行tfidf表示
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return dictionary,corpus,corpus_tfidf

# 使用lda模型，获取主题分布
def lda_model(dictionary,corpus,corpus_tfidf,num_topics,file_path):   
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    f_keyword = open(file_path, 'w', encoding='utf-8')
    for topic in lda.print_topics(num_topics=num_topics,num_words=50):
        print( '****'*5, topic[0], '****'*5)
        words=[]
        for word in topic[1].split('+'):
            word = word.split('*')[1].replace(' ','')
            words.append(word)
        f_keyword.write(str(topic[0])+'\t'+','.join(words)+'\n')
    #利用lda模型，对文本进行向量表示，这相当于与tfidf文档向量表示进行了降维，维度大小是设定的主题数目  
#    corpus_lda = lda[corpus_tfidf]
#    for doc in corpus_lda:
#        print( len(doc),doc)   
    return lda

# 使用lsi模型，获取主题分布
def lsi_model(dictionary,corpus,corpus_tfidf,num_topics, cluster_keyword_lsi):
    lsi = models.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    f_keyword = open(cluster_keyword_lsi, 'w', encoding='utf-8')
    for topic in lsi.print_topics(num_topics=num_topics,num_words=50):
        print('****'*5, topic[0], '****'*5)
        words=[]
        for word in topic[1].split('+'):
            word=word.split('*')[1].replace(' ','')
            words.append(word)
        f_keyword.write(str(topic[0])+'\t'+','.join(words)+'\n')
   
    return lsi

## main
if __name__=='__main__':
    cluster_keyword_lda_filepath = './data_out/cluster_keywords_lda.txt'   
    cluster_keyword_lsi_filepath = './data_out/cluster_keywords_lsi.txt'
    corpus_path = './data/self_info_results_all.xls'
    dictionary,corpus,corpus_tfidf = create_data(corpus_path)
    lda = lda_model(dictionary,corpus,corpus_tfidf,6,cluster_keyword_lda_filepath)
    lsi = lsi_model(dictionary,corpus,corpus_tfidf,6,cluster_keyword_lsi_filepath)

    # show cluster keywords for LDA
    f = open(cluster_keyword_lda_filepath,'r', encoding='utf-8')
    cluster_keyword_lda = f.read()
    print(cluster_keyword_lda)
    f.close()
    
    
    # test 
    test_data = open('./data/test_chictr.txt','r',encoding='utf-8-sig').readlines()
    test_dictionary,test_corpus,test_corpus_tfidf = data_process(test_data)
    topics_test = lda.get_document_topics(test_corpus)
    for i in range(len(test_data)):
        print(i, 'topic distribution: ',topics_test[i],'\n')
