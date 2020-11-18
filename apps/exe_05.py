# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:25:50 2020

@author: Xu


5.用户评价情感分析

根据


负责响应数据查询请求，调用数据逻辑程序。
基于数据逻辑查询结果，业务逻辑程序组装出用户评价文本的分析数据并返回给前端页面。

"""
import os
import sys
import pandas as pd
import config
sys.path.append(r'D:\PythonJupyterNootebook\My NLP projects\My projects\NLPVisualizationSystem\model')
from review_sentiment_analysis import review_summary

# 5.用户评价情感分析
# 数据逻辑：
def save_to_file(filepath, content):
    """
    Write the text to the local file.

    Parameters
    ----------
    filepath : TYPE-str
        DESCRIPTION: the file save path.

    Returns
    -------
    content : TYPE-str
        DESCRIPTION: the text.

    """
    f = open(filepath, 'w', encoding='utf-8') 
    f.write(content)
    f.close()

def read_file(filepath):
    """
    Read the local file and transform to text.

    Parameters
    ----------
    filepath : TYPE-str
        DESCRIPTION: the text file path.

    Returns
    -------
    content : TYPE-str
        DESCRIPTION:The preprocessed news text.

    """
    f = open(filepath,'r',encoding='utf-8')
    content = f.read()
    f.close()
    return content   
    
def rt_index_query():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    # load data
    data = pd.read_csv(config.business_data_path)
    data2 = pd.read_csv(config.review_data_path)
    # select data
    product_sum = data.shape[0]
    user_sum = len(data2['user_name'].unique())
    review_sum = data2.shape[0]
    return product_sum, user_sum, review_sum


def review_summary_query():
    """
    According to the query information entered by the user, 
    the product review summary is returned.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    data = pd.read_csv(config.review_data_path)
    query_word = read_file(config.user_input_id_name_path).strip()
    if query_word.isnumeric()==False:
        product_id = data.loc[(data['product_name']==query_word), 'product_id'].values[0]
        product_name, product_basic, review_result = review_summary(product_id, config.review_summary_save_path)
    else:
        product_name, product_basic, review_result = review_summary(int(query_word), config.review_summary_save_path)
    return  product_name, product_basic, review_result
        
        

# 业务逻辑：

def rt_index_base():
    """
    It is used to get the data of realtime index.

    Returns
    -------
    cur : TYPE-dict
        realt-time index.

    """
    product_sum, user_sum, review_sum = rt_index_query()
    cur = {"product_sum": product_sum, "user_sum": user_sum, "review_sum": review_sum}
    return cur


def review_summary_base():
    product_name, product_basic, review_result = review_summary_query()
    cur = {'product_name': product_name, 'product_basic': product_basic, 'review_result': review_result}
    return cur
    

def download_review_summary_base():
    path = config.review_summary_save_path
    file_dir, filename = os.path.split(path)
    return file_dir, filename









