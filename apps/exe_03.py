# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:01:58 2020

@author: Xu

3.文本关键信息提取
单文本分析：
基于TextRank的算法的单文本摘要提取与关键词抽取。

多文本分析：
基于LDA的多文档主题分布探索。



负责响应数据查询请求，调用数据逻辑程序。
基于数据逻辑查询结果，业务逻辑程序组装出文本关键信息并返回给前端页面。


"""

import os
import sys
import re
import config
from newspaper import Article
sys.path.append(r'D:\PythonJupyterNootebook\My NLP projects\My projects\NLPVisualizationSystem\model')
from keywords_textrank import TextRank
from abstract_textrank import AbstarctTextrank
from topic_cluster_lda import lda_model


# 3. 文本关键信息提取--- Part 1 单文本分析 
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


def get_webcontent(url):
        """
        Online mode: According to the URL, grab the text content of the news.

        Parameters
        ----------
        url : TYPE-str
            DESCRIPTION: news online URL.

        Returns
        -------
        content : TYPE-str
            DESCRIPTION:The preprocessed news text.

        """
        news = Article(url, language='zh')
        news.download()
        news.parse()
        content = news.text
        return content


def get_abstract(text):  
    """
    Use Textrank algorithm to extract text summaries/abstract.
    
    Parameters
    ----------
    text : TYPE-str
        DESCRIPTION: the text content to be extracted.

    Returns
    -------
    abstract : TYPE-str
        DESCRIPTION: the abstract extracted from text.
    
    """
    abstracter = AbstarctTextrank()
    keysentences = abstracter.extract_abstract(text, 3)
    abstract = []
    for sent in keysentences:
        abstract.append(sent[0])     
    return abstract

def get_keywords(text):
    """
    Use Textrank algorithm to extract text keywords.
    
    Parameters
    ----------
    text : TYPE-str
        DESCRIPTION: the text content to be extracted.

    Returns
    -------
    words : TYPE-str
        DESCRIPTION: the keywords extracted from text.
    
    """
    keywords_textanker = TextRank()
    keywords = keywords_textanker.extract_keywords(text, 10)
    words = []
    for word in keywords:
        words.append(word[0])
    return words 




def keyinfo_by_url_query():
    """
    According to the user's input to specify the URL, the text of the URL is collected, 
    and an abstract and keywords are automatically generated.

    Returns
    -------
        abstract:TYPE-strs
            DESCRIPTION: the abstract extracted from text.
        keywords:TYPE-strs
            DESCRIPTION: the keywords extracted from text.

    """
    url = read_file(config.keyinfo_input_url_path)
    content = get_webcontent(url)
    abstract = get_abstract(content)
    keywords = get_keywords(content)
    abstract = '。 '.join(abstract) + '。'
    keywords = ', '.join(keywords)
    wr_to_file = '摘要：\n' + abstract + '\n关键词：\n' + keywords
    save_to_file(config.download_keyinfo_input_url_save_path, wr_to_file)
    return abstract, keywords
    

def keyinfo_by_input_text_query():
    """
    According to the text input by the user, an abstract and keywords 
    are automatically generated.

    Returns
    -------
        abstract:TYPE-strs
            DESCRIPTION: the abstract extracted from text.
        keywords:TYPE-strs
            DESCRIPTION: the keywords extracted from text.

    """
    input_text = read_file(config.keyinfo_input_text_path)
    abstract = get_abstract(input_text)
    keywords = get_keywords(input_text)
    abstract = '。 '.join(abstract) + '。'
    keywords = ', '.join(keywords)
    wr_to_file = '摘要：\n' + abstract + '\n关键词：\n' + keywords
    save_to_file(config.download_keyinfo_input_text_save_path, wr_to_file)
    return abstract, keywords


def keyinfo_by_import_file_query():
    """
    According to the local file imported by the user, an abstract and keywords 
    are automatically generated.

    Returns
    -------
        abstract:TYPE-strs
            DESCRIPTION: the abstract extracted from text.
        keywords:TYPE-strs
            DESCRIPTION: the keywords extracted from text.

    """
    path = read_file(config.keyinfo_input_file_save_path).strip()
    content = read_file(path)
    abstract = get_abstract(content)
    keywords = get_keywords(content)
    abstract = '。 '.join(abstract) + '。'
    keywords = ', '.join(keywords)
    wr_to_file = '摘要：\n' + abstract + '\n关键词：\n' + keywords
    save_to_file(config.download_keyinfo_input_file_save_path, wr_to_file)
    return abstract, keywords




# 业务逻辑：
   
def rt_keyinfo_url_base():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    url = read_file(config.keyinfo_input_url_path)
    abstract, keywords = keyinfo_by_url_query()
    curinput = {'url': url, 'abstract': abstract, 'keywords': keywords}
    return curinput




def rt_keyinfo_input_text_base():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    input_text = read_file(config.keyinfo_input_text_path)
    abstract, keywords = keyinfo_by_input_text_query()
    curinput = {'input_text':input_text, 'abstract': abstract, 'keywords': keywords }
    return curinput

def download_rt_keyinfo_import_file_base():
    path = read_file(config.keyinfo_input_file_save_path).strip()
    file_dir, filename = os.path.split(path)
    return file_dir, filename


def rt_keyinfo_import_file_base():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    path = read_file(config.keyinfo_input_file_save_path).strip()
    filename = os.path.split(path)[-1]
    abstract, keywords = keyinfo_by_import_file_query()
    curinput = {'filename':filename, 'abstract': abstract, 'keywords': keywords}
    return curinput



# 3. 文本关键信息提取--- Part 2 多文本分析 
# 数据逻辑：
def lda_topics_query():
    """
    It is used to get the optimal number of topics  and save the topic keywords  and 
    topic distribution of documents to a file based on the file imported by the user.
    
    Returns
    -------
    num_topics: type-integer
        return the number of topics.
    
    
    """
    # data prepare
    filepath = read_file(config.topic_input_file_save_path).strip()
    f = open(filepath, 'r', encoding='utf-8')
    content = f.readlines()
    f.close()
    data = [text for text in content if len(re.sub(r'\s','',text))>5]
    # get optimal number of topics 
    # write topic keywords to file 
    num_topics, output_topic_keywords,  output_topic_dist = lda_model(data, config.download_topic_input_file_save_path)                     
    return num_topics, output_topic_keywords,  output_topic_dist



# 业务逻辑：
def rt_topic_import_file_base():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    path = read_file(config.topic_input_file_save_path).strip()
    filename = os.path.split(path)[-1]
    num_topics, topic_keywords,  topic_dist = lda_topics_query()
    curinput = {'filename':filename, 'num_topics':num_topics, 'topic_keywords': topic_keywords, 'topic_dist': topic_dist}
    return curinput

























