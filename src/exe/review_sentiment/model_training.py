# 此文件包含模型的训练。 给定数据集，训练出情感分类模型，并把模型文件存放在 model文件夹里。
import json
import numpy as np
import pandas as pd
import business
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import pos_tag, word_tokenize
# from glove_embedding import GloveEmbedding
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import utils
from utils import handle_text
from embedding_manager_cyd import EmbeddingManagerCyd
from embedding_manager_cyd import Embedding_Type

SEED = 222
np.random.seed(SEED)

dic_business_id = {}

def main():

    embeddingManagerCyd = EmbeddingManagerCyd()

    json_file_business_path = './data/business.json'
    json_file_review_path = './data/review.json'

    with open(json_file_business_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            line_contents = json.loads(line)
            business_id = line_contents["business_id"]
            name = line_contents["name"]
            review_count = line_contents["review_count"]
            dic_business_id[business_id] = []

    tags = []
    reviewList = []
    sentiment = 0
    index = 0

    with open(json_file_review_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            line_contents = json.loads(line)
            business_id = line_contents["business_id"]
            if business_id in dic_business_id:
                review_id = line_contents["review_id"]
                user_id = line_contents["user_id"]
                stars = line_contents["stars"]
                text = line_contents["text"]
                if stars >= 4:
                    sentiment = 1
                else:
                    sentiment = 0
                tags.append(sentiment)
                # reviewList.append([index,text])
                # reviewList.append(handle_text(text))
                reviewList.append(embeddingManagerCyd.getEmbedding(text, Embedding_Type.glove, True, False))
                index += 1
                print(index)
                # if index >= 20000:
                #     break


    # glove_embedding = GloveEmbedding()
    # # gloveVectors = [glove_embedding.getSentenceVectorCommon(item[1], isUseAveragePooling=True) for item in tokenizedWords.items()]
    # gloveVectors = [glove_embedding.getSentenceVectorCommon(item, isUseAveragePooling=True) for item in
    #                 reviewList]
    # features = np.array(gloveVectors, dtype=np.float16)

    features = np.array(reviewList, dtype=np.float16)
    tags = np.array(tags)

    classification_svm(features, tags)
    # classification_logistic(features, tags)

    # print("step4=================")

def get_train_test(features,tags,test_size=0.3):
    return train_test_split(features, tags, test_size=test_size, random_state=SEED)

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.externals import joblib #jbolib模块
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

def classification_logistic(features, tags):
    xtrain, xtest, ytrain, ytest = get_train_test(features, tags)

    # cross_validator = KFold(n_splits=10, shuffle=False, random_state=None)

    # lr = LogisticRegression(penalty = "l1")
    #
    # # params = {"penalty":["l1","l2"],
    # #              "C":[0.1,1.0,10.0,100.0]},
    #
    # params = {"C":[100, 120,150]},

    # grid = GridSearchCV(estimator=lr, param_grid = params)
    # grid.fit(xtrain, ytrain)
    # print("最优参数为：",grid.best_params_)
    # model = grid.best_estimator_
    # predict_value = model.predict(xtest)
    # proba_value = model.predict_proba(xtest)
    # p = proba_value[:,1]
    # print("Logistic=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))
    #
    # joblib.dump(model, 'model/logistic_clf.pkl')

    model = LogisticRegression(penalty="l1",C = 100, solver='liblinear')
    model.fit(xtrain, ytrain)
    predict_value = model.predict(xtest)
    proba_value = model.predict_proba(xtest)
    p = proba_value[:,1]
    print("Logistic=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))
    joblib.dump(model, 'model/logistic_clf.pkl')

    #100000 0.889
    #50000 0.889

def classification_svm(features, tags):
    xtrain, xtest, ytrain, ytest = get_train_test(features, tags)

    # svc = SVC(kernel='rbf',probability = True)
    # model = make_pipeline(svc)
    #
    # # 使用GridSearchCV选择参数
    # # param_grid = {'svc__C': [1, 5, 10,0.5,20,30],
    # #               'svc__gamma': [0.0001, 0.0005, 0.001, 0.005,0.006,0.007,0.008,0.009,0.01]}
    # param_grid = {'svc__C': [1, 5, 10, 15],
    #               'svc__gamma': [0.0005, 0.001, 0.005]}
    # grid = GridSearchCV(model, param_grid)
    #
    # grid.fit(xtrain, ytrain)
    # print("最优参数为：",grid.best_params_)
    # model = grid.best_estimator_
    # predict_value = model.predict(xtest)
    # proba_value = model.predict_proba(xtest)
    # p = proba_value[:,1]
    # print("SVM=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))

    model =SVC(kernel='rbf',probability = True, C=20, gamma=0.005)
    model.fit(xtrain, ytrain)
    proba_value = model.predict_proba(xtest)
    p = proba_value[:, 1]
    print("SVM=========== ROC-AUC score: %.3f" % roc_auc_score(ytest, p))
    joblib.dump(model, 'model/svm_clf.pkl')

    #20000 0.883
    #500000 0.887

if __name__ == "__main__":
    main()

