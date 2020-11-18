# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:34:05 2020

@author: Xu
"""


# ###########################################################################
# 提取评价关键信息
import config 
import pandas as pd
import numpy as np
import nltk
import sentiment_model
from sentiment_model import SentimentModel

# 自定义打印方法
def print_format(str, a):
    print(str + '\n{0}\n'.format(a))
    
# review对应的数据类
class ReviewDataItem(object):
    def __init__(self, review_id, user_name, product_id, rates, text):
        self.review_id = review_id
        self.user_name = user_name
        self.product_id = product_id
        self.rates = rates
        self.text = text


# product对应的数据类
class ProductDataItem(object):
    def __init__(self, product_id, product_name, review_count):
        self.product_id = product_id
        self.product_name = product_name
        self.review_count = review_count



class Business(object):
    """
    用来表示跟business相关的变量和函数
    """

    def __init__(self):
        # 初始化变量以及函数
        # self.aspect_filter = ["salsa"]
        self.aspect_filter = []
        self.dic_business_id = {}
        self.dic_business_data = {}
        print("step1 加载模型==================")
        self.sentimentModel = SentimentModel()  # 把已经训练好的模型存放在文件里，并导入进来
        print("step2 读取数据开始==================")
        self.read_data()
        print("step2 读取数据结束==================")

    def read_data(self):

        review_data = pd.read_csv(config.review_data_path)
        product_data = pd.read_csv(config.business_data_path)
        
        for index in product_data.index:
            product_id = product_data.loc[index, "product_id"]
            product_name = product_data.loc[index,"product_name"]
            review_count = product_data.loc[index,"review_count"]
            if review_count >= 2:
                self.dic_business_id[product_id] = []
                business_DataItem = ProductDataItem(product_id, product_name, review_count)
                self.dic_business_data[product_id] = business_DataItem

        for index in review_data.index:
            product_id = review_data.loc[index, "product_id"]    
            if product_id in self.dic_business_id:
                review_id = review_data.loc[index, "review_id"]
                user_name = review_data.loc[index, "user_name"]
                rates = review_data.loc[index,['rating_overall', 'rating_ease_of_use',
                                               'rating_customer_support','rating_features_functionality',
                                               'rating_value_for_money','rating_likelihood_to_recommend']].T.to_dict()
                text = review_data.loc[index, "review"]
                review_DataItem = ReviewDataItem(review_id, user_name, product_id, rates, text)
                self.dic_business_id[product_id].append(review_DataItem)

            

    def aspect_based_summary(self, business_id):
        """
        返回一个business的summary. 针对于每一个aspect计算出它的正面负面情感以及TOP reviews.
        具体细节请看给定的文档。
        """

        aspects_dic = self.extract_aspects(business_id)        
        business_name = self.dic_business_data[business_id].product_name        

        pos_aspect_dic = {}
        neg_aspect_dic = {}
        review_segment_dic = {}

        for aspect, reviews in aspects_dic.items():
            for review in reviews:
                review_text = review.text
                if review_text == None or str.strip(review_text) == '':
                    continue
                review_segment = self.get_segment(review_text, aspect, aspects_dic)
                # 粗略筛选一下
                if len(str.strip(review_segment)) > len(aspect) + 3:
                    print(review_segment)
                    key = str(review.review_id) + "_" + aspect
                    review_segment_dic[key] = review_segment

                    score = self.sentimentModel.predict_prob(review_segment)

                    if score > 0.7:
                        if aspect not in pos_aspect_dic:
                            pos_aspect_dic[aspect] = []
                        pos_aspect_dic[aspect].append([key, score])
                    else:
                        if aspect not in neg_aspect_dic:
                            neg_aspect_dic[aspect] = []
                        neg_aspect_dic[aspect].append([key, score])

        dic_aspect_summary = {}
        for aspect, reviews in aspects_dic.items():
            if aspect not in dic_aspect_summary:
                dic_aspect_summary[aspect] = {}

            # 算某个aspect的得分
            try:
                pos_aspect_review_nums = len(pos_aspect_dic[aspect])
                pos_aspect_total_scores = 0
                for item in pos_aspect_dic[aspect]:
                    pos_aspect_total_scores += item[1]
            except:
                pos_aspect_review_nums = 0
                pos_aspect_total_scores = 0
                        
            try:
                neg_aspect_review_nums = len(neg_aspect_dic[aspect])
                neg_aspect_total_scores = 0
                for item in neg_aspect_dic[aspect]:
                    neg_aspect_total_scores += item[1]
            except:
                neg_aspect_review_nums = 0
                neg_aspect_total_scores = 0
            
            aspect_review_nums = pos_aspect_review_nums + neg_aspect_review_nums if pos_aspect_review_nums + neg_aspect_review_nums>0 else 1 
            
            aspect_score = (pos_aspect_total_scores + neg_aspect_total_scores) / aspect_review_nums

            dic_aspect_summary[aspect]["rating"] = aspect_score

            # TOP 5 正面
            if aspect in pos_aspect_dic:
                aspects_pos_sorted = sorted(pos_aspect_dic[aspect], key=lambda x: x[1], reverse=True)
                aspects_pos_contents = {}
                dic_aspect_summary[aspect]["pos"] = []
                for index, item in enumerate(aspects_pos_sorted):
                    if len(dic_aspect_summary[aspect]["pos"]) >= 5:
                        break
                    review_content = review_segment_dic[item[0]]
                    if review_content not in aspects_pos_contents:
                        dic_aspect_summary[aspect]["pos"].append(review_content)
                        aspects_pos_contents[review_content] = None
            else:
                dic_aspect_summary[aspect]["pos"] = ['None']
                

            # TOP 5 负面
            if aspect in neg_aspect_dic:
                aspects_neg_sorted = sorted(neg_aspect_dic[aspect], key=lambda x: x[1], reverse=False)
                aspects_neg_contents = {}
                dic_aspect_summary[aspect]["neg"] = []
                for index, item in enumerate(aspects_neg_sorted):
                    if len(dic_aspect_summary[aspect]["neg"]) >= 5:
                        break
                    review_content = review_segment_dic[item[0]]
                    if review_content not in aspects_neg_contents:
                        dic_aspect_summary[aspect]["neg"].append(review_content)
                        aspects_neg_contents[review_content] = None
            else:
                dic_aspect_summary[aspect]["neg"] = ['None']

        all_aspect_scores = 0
        for item in dic_aspect_summary.items():
            all_aspect_scores += item[1]["rating"]

        business_rating = all_aspect_scores / len(dic_aspect_summary.items())
        average_user_rating = self.dic_business_id[business_id][0].rates

        return {'business_id':business_id,
            'business_name':business_name,
            'business_rating':business_rating,
            'average_user_rating':average_user_rating,
            'aspect_summary':dic_aspect_summary
            }

    def get_segment(self, review_text, aspect, aspects_dic):

        if self.is_review_only_one_aspect(review_text):
            return review_text

        cur_aspect_index = review_text.index(aspect)
        cur_aspect_end_index_begin = cur_aspect_index + len(aspect)
        cur_aspect_end_index_end = cur_aspect_end_index_begin
        end_pos = len(review_text) - 1

        stop_punct_map = {c: None for c in ',.!?;'}
        relation_punct_list = ["and", "when", "but"]

        # next_aspect = self.get_next_aspect(review_text[cur_aspect_end_index_begin:end_pos])
        cur_aspect_des = self.get_cur_aspect_adj(review_text[cur_aspect_end_index_begin:end_pos])

        while cur_aspect_end_index_end <= end_pos:
            # 在标点符号处截取
            cur_str = review_text[cur_aspect_end_index_end:min(cur_aspect_end_index_end + 1, end_pos)]
            if cur_str in stop_punct_map:
                break

            # 在转移符号处截取
            cur_strs = review_text[cur_aspect_end_index_begin:cur_aspect_end_index_end]
            relation_store = ""
            for relation in relation_punct_list:
                if relation in cur_strs.lower():
                    relation_store = relation
                    break

            if relation_store != "":
                cur_aspect_end_index_end -= len(relation_store)
                break

            # 在下一个aspect截取
            # if next_aspect != None:
            # 	if next_aspect in aspects_dic and next_aspect in cur_strs:
            # 		cur_aspect_end_index_end -= len(next_aspect)
            # 		break

            # 在aspect最近的形容词截取
            if cur_aspect_des != None:
                if cur_aspect_des in cur_strs:
                    break

            cur_aspect_end_index_end += 1

        cur_aspect_end_index_end = min(cur_aspect_end_index_end, end_pos)
        return review_text[cur_aspect_index:cur_aspect_end_index_end]

    def get_next_aspect(self, text):
        tokens = nltk.word_tokenize(text)
        tag_tuples = nltk.pos_tag(tokens)
        for (word, tag) in tag_tuples:
            if tag == "NN":
                return word
        return None

    def get_cur_aspect_adj(self, text):
        tokens = nltk.word_tokenize(text)
        tag_tuples = nltk.pos_tag(tokens)
        for (word, tag) in tag_tuples:
            if tag == "JJ" or tag == "ADJ":
                return word
        return None

    def is_review_only_one_aspect(self, review_text):
        '''
        判断评论里面是否只包含一个方面
        :param review:
        :return:
        '''

        tagged_words = []
        tokens = nltk.word_tokenize(review_text)
        tag_tuples = nltk.pos_tag(tokens)
        for (word, tag) in tag_tuples:
            if tag == "NN":
                tagged_words.append(word)

        if len(tagged_words) <= 1:
            return True

        return False

    def extract_aspects(self, business_id):
        """
        从一个business的review中抽取aspects
        """

        # print("step3 extract_aspects begin==================")

        if business_id not in self.dic_business_id:
            print("business_id not exit")
            return None

        review_list = self.dic_business_id[business_id]
        aspects_dic = {}
        for review_data in review_list:
            sentence = review_data.text
            if sentence == None or str.strip(sentence) == '':
                continue
            tagged_words = []
            tokens = nltk.word_tokenize(sentence)
            tag_tuples = nltk.pos_tag(tokens)
            for (word, tag) in tag_tuples:
                if tag == "NN":
                    # token = {'word': string, 'pos': tag}
                    # tagged_words.append(word)
                    if word not in aspects_dic:
                        aspects_dic[word] = []
                    aspects_dic[word].append(review_data)

        # 对字典进行排序
        aspects_sorted = sorted(aspects_dic.items(), key=lambda x: len(x[1]), reverse=True)
        aspects_dic = {}
        for index, item in enumerate(aspects_sorted):
            if item[0] in self.aspect_filter:
                continue

            if len(aspects_dic.items()) < 5:
                aspects_dic[item[0]] = item[1]

        # print("step3 extract_aspects end==================")
        return aspects_dic

# ###########################################################################
# 文本数据增强：UDA-处理样本不平衡
# 正面和负面评价数量占比约为8:1（评分大于4为正面，小于等于4为负面）
def review_data_augmentation(text):
    return 












# #################################################################################
# 构建二分类情感分析模型
# sentiment classification model train
from nltk import pos_tag, word_tokenize
from glove_embedding import GloveEmbedding
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import utils
from utils import handle_text
from embedding_manager_cyd import EmbeddingManagerCyd
from embedding_manager_cyd import Embedding_Type
from textblob import TextBlob

SEED = 222
np.random.seed(SEED)

dic_business_id = {}

def train_model():

    embeddingManagerCyd = EmbeddingManagerCyd()
    
    review_data = pd.read_csv(config.review_data_path)
    product_data = pd.read_csv(config.business_data_path)
    
    for index in product_data.index:
        product_id = product_data.loc[index, "product_id"]
        product_name = product_data.loc[index,"product_name"]
        review_count = product_data.loc[index,"review_count"]
        dic_business_id[product_id] = []
        
    tags = []
    reviewList = []
    sentiment = 0
    index = 0

    for index in review_data.index:
        product_id = review_data.loc[index, "product_id"]    
        if product_id in dic_business_id:
            review_id = review_data.loc[index, "review_id"]
            user_name = review_data.loc[index, "user_name"]
            rates = review_data.loc[index,['rating_overall', 'rating_ease_of_use',
                                           'rating_customer_support','rating_features_functionality',
                                           'rating_value_for_money','rating_likelihood_to_recommend']].T.to_dict()
            text = review_data.loc[index, "review"]
#            # 分类标准：用户平均评分>4为1，<=4为0
#            if np.mean(list(rates.values())) > 4:
#                sentiment = 1
#            else:
#                sentiment = 0
            
            # 分类标准：根据textblob对语义进行情感极性判断
            blob = TextBlob(text)
            if blob.sentiment.polarity > 0.2:
                sentiment = 1
            else:
                sentiment = 0
            
            tags.append(sentiment)
            reviewList.append(embeddingManagerCyd.getEmbedding(text, Embedding_Type.glove, True, False))
            index += 1
            print(index)

#    glove_embedding = GloveEmbedding()
#    #gloveVectors = [glove_embedding.getSentenceVectorCommon(item[1], isUseAveragePooling=True) for item in tokenizedWords.items()]
#    gloveVectors = [glove_embedding.getSentenceVectorCommon(item, isUseAveragePooling=True, isUseStopwords=False) for item in reviewList]
#    features = np.array(gloveVectors, dtype=np.float16)

    features = np.array(reviewList, dtype=np.float16)
    tags = np.array(tags)

    classification_svm(features, tags)
    classification_logistic(features, tags)

    print("step4=================")

def get_train_test(features,tags,test_size=0.3):
    return train_test_split(features, tags, test_size=test_size, random_state=SEED)

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.externals import joblib #jbolib模块
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

def classification_logistic(features, tags):
    xtrain, xtest, ytrain, ytest = get_train_test(features, tags)

## 使用GridSearchCV选择参数
#    cross_validator = KFold(n_splits=10, shuffle=False, random_state=None)
#    lr = LogisticRegression(penalty = "l1")
#    params = {"penalty":["l1","l2"],
#              "C":[0.1,1.0,10.0,100.0, 120, 150]}
#
#    grid = GridSearchCV(estimator=lr, param_grid = params)
#    grid.fit(xtrain, ytrain)
#    print("最优参数为：",grid.best_params_)
#    model = grid.best_estimator_
#    predict_value = model.predict(xtest)
#    proba_value = model.predict_proba(xtest)
#    p = proba_value[:,1]
#    print("Logistic=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))   
#    joblib.dump(model, config.lr_model_save_path)

    model = LogisticRegression(penalty="l1",C = 100, solver='liblinear')
    model.fit(xtrain, ytrain)
    predict_value = model.predict(xtest)
    proba_value = model.predict_proba(xtest)
    p = proba_value[:,1]
    print("Logistic=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))
    joblib.dump(model, config.lr_model_save_path)

    

def classification_svm(features, tags):
    xtrain, xtest, ytrain, ytest = get_train_test(features, tags)

#    # 使用GridSearchCV选择参数
#    svc = SVC(kernel='rbf',probability = True)
#    model = make_pipeline(svc)
#    param_grid = {'svc__C': [0.5, 1, 5, 10, 15, 20, 25, 30],
#                  'svc__gamma': [0.0001, 0.0005, 0.001, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.1]}
#    grid = GridSearchCV(model, param_grid)   
#    grid.fit(xtrain, ytrain)
#    print("最优参数为：",grid.best_params_)
#    model = grid.best_estimator_
#    predict_value = model.predict(xtest)
#    proba_value = model.predict_proba(xtest)
#    p = proba_value[:,1]
#    print("SVM=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))
#    joblib.dump(model, config.svm_model_save_path)

    model = SVC(kernel='rbf',probability = True, C=20, gamma=0.005)
    model.fit(xtrain, ytrain)
    proba_value = model.predict_proba(xtest)
    p = proba_value[:, 1]
    print("SVM=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))
    joblib.dump(model, config.svm_model_save_path)

#train_model()



def review_summary(product_id, filepath):
    """
    According to the input product ID number, summarize the user's evaluation of the product.
    
    parameters: 
        product_id: type-int, product id
        filepath: type-int, the file save path
        
    --------------    
    return:
        product_basic: type_str, product info
        review_result: type_str, review summary
    
    """
    b = Business()   
    summary = b.aspect_based_summary(product_id)
    product_name = b.dic_business_data[product_id].product_name
    normal_print_list = ["business_id","business_name","business_rating", 'average_user_rating', "rating"]
    f = open(filepath, 'w', encoding='utf-8')
    product_basic = ''
    review_result = ''
    for item in summary.items():
        if item[0] in normal_print_list:
            print(str(item[0]) + ": " + str(item[1]))
            f.write(str(item[0]) + ": " + str(item[1]) + '\n')
            product_basic += str(item[0]) + ": " + str(item[1]) + '\n'
        else:
            print(str(item[0]) + ": ")
            f.write(str(item[0]) + ": " + '\n')
            review_result += str(item[0]) + ": " + '\n'
            for data in item[1].items():               
                print("------------------" + str(data[0]) + "------------------")
                f.write("------------------" + str(data[0]) + "------------------" + '\n')
                review_result += "------------------" + str(data[0]) + "------------------" + '\n'
                for data_1 in data[1].items():
                    if data_1[0] in normal_print_list:
                        print(str(data_1[0]) + ": " + str(data_1[1]))
                        f.write(str(data_1[0]) + ": " + str(data_1[1]) + '\n')
                        review_result += str(data_1[0]) + ": " + str(data_1[1]) + '\n'
                    else:
                        review_list = []
                        for item_1 in data_1[1]:
                            review_list.append(item_1)
                        print(str(data_1[0]) + ": " + ";  ".join(review_list))
                        f.write(str(data_1[0]) + ": " + ";  ".join(review_list) + '\n')
                        review_result += str(data_1[0]) + ": " + ";  ".join(review_list) + '\n'
    f.close()
    return product_name, product_basic, review_result
    
        
    
    
    

if __name__ == "__main__":   
    product_name, product_basic, review_result = review_summary(4, 'review_summary.txt')
    








