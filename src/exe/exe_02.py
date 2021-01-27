# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 17:34:12 2020

@author: Xu


2.自动生成词云图：
负责响应数据查询请求，调用数据逻辑程序。
基于数据逻辑查询结果，业务逻辑程序组装出词云图并返回给前端页面。

三种类型的高频词和关键词可视化：

根据用户输入指定网址，通过采集该网址文本进行处理。
根据用户输入文本字符串进行处理。
根据用户输入载入本地文本进行处理，用户将所需要处理文本文件放入text文本夹中，指定文件名进行处理。

"""
import __init__
import os
import numpy as np
from src import config
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.render import make_snapshot
from jieba import posseg 
# import wordcloud 
from newspaper import Article
# from imageio import imread
from snapshot_selenium import snapshot

# 2. 自动生成词云
# 数据逻辑：
def save_to_file(filepath, content):
    f = open(filepath, 'w', encoding='utf-8') 
    f.write(content)
    f.close()
    
def extract_words(content):
    """
    Statistical word frequency.

    Parameters
    ----------
    content : TYPE-str
        DESCRIPTION: text.

    Returns
    -------
    word_dict : TYPE-dictionary
        DESCRIPTION: dictionary like {Word1: Frequency1, Word2: Frequency2} .

    """
    words = []
    pos_filters = ['n', 'v', 'a']
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        words += [w.word for w in posseg.cut(line) if w.flag[0] in pos_filters and len(w.word) > 1]
    word_dict = {i[0]: i[1] for i in Counter(words).most_common()}
    return word_dict
 
    
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


def get_sorted_dict(dic, topn=100):
    """
    Sort the dictionary by value and take the top n with the largest value.
    
    Parameters:
        dic: TYPE-dictionary
            DESCRIPTION: Dictionary to be sorted.
        topn: TYPE-integer
            DESCRIPTION: Select the N (key: value) with the largest value (default = 100).

    Returns
    -------
    res : TYPE-list
        DESCRIPTION: A list composed of the top N key-value combinations after sorting, 
        like [('a', 101),('b',78),...].
    
    """
    res = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    if topn > len(dic):
         return res
    else: 
         return res[0: topn]
    
    
def text_wordfreq_by_url_query():
    """
    According to the user's input to specify the URL, the text of the URL is collected, 
    and a word cloud image is automatically generated.

    Returns
    -------
        word_dict:TYPE-dictionary
            DESCRIPTION: dictionary like {Word1: Frequency1, Word2: Frequency2} .

    """
    
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
    
    url = read_file(config.wc_input_url_path)
    content = get_webcontent(url)
    word_dict = extract_words(content)
    return word_dict
    
    
 
def text_wordfreq_by_input_query():
    """
    According to the text input by the user, a word cloud image is automatically generated.
    
    Parameters:
        input_text: TYPE-str
            DESCRIPTION: the text input by the user.

    Returns
    -------
        word_dict:TYPE-dictionary
            DESCRIPTION: dictionary like {Word1: Frequency1, Word2: Frequency2} .

    """
    input_text = read_file(config.wc_input_text_path)
    word_dict = extract_words(input_text)
    return word_dict
    
    
    
    
    
def text_wordfreq_by_import_file_query():    
    """
    According to the local file imported by the user, the word cloud image 
    is automatically generated.
    
    Parameters:
        textfile: TYPE-str
            DESCRIPTION: the text file imported by user.


    Returns
    -------
        word_dict:TYPE-dictionary
            DESCRIPTION: dictionary like {Word1: Frequency1, Word2: Frequency2} .

    """
    path = read_file(config.wc_input_file_save_path).strip()
    content = read_file(path)
    word_dict = extract_words(content)
    return word_dict
    
    
    

# 业务逻辑：
def pic_rt_user_url_base():
    path = config.pic_wc_input_url_save_path
    file_dir, filename = os.path.split(read_file(path).strip())
    return file_dir, filename
    

    
def rt_user_url_base():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    userurl = read_file(config.wc_input_url_path)
    curinput = {'userurl': userurl}
    return curinput

def pic_rt_user_input_text_base():
    path = config.pic_wc_input_text_save_path
    file_dir, filename = os.path.split(read_file(path).strip())
    return file_dir, filename



def rt_user_input_text_base():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    usertext = read_file(config.wc_input_text_path)
    curinput = {'usertext':usertext }
    return curinput

def pic_rt_user_import_file_base():
    path = config.pic_wc_input_file_save_path
    file_dir, filename = os.path.split(read_file(path).strip())
    return file_dir, filename



def rt_user_import_file_base():
    """
    It is used to return the requested real-time data.

    Returns
    -------
    curinput : TYPE-dictionary
        return the frontend requested real-time data.
    
    """
    path = read_file(config.wc_input_file_save_path).strip()
    filename = os.path.split(path)[-1]
    curinput = {'userfile':filename}
    return curinput


def generate_random_filename(prefix, suffix):
    """
    According to the specified prefix name and suffix name, 
    this function is used to generate a random file name.
    Parameters:
        prefix: TYPE-str
            DESCRIPTION: Specified prefix name.
        suffix: TYPE-str
            DESCRIPTION: Specified suffix name.
    Returns
    -------
    random_filename : TYPE-str
        return the random file name.
    
    """
    randnum = np.random.randint(1, 100000)
    random_filename = prefix + '_' + str(randnum) + suffix
    return random_filename
    




def wordcloud_text_by_url_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    
    # data query    
    data = text_wordfreq_by_url_query()
    data_pair = get_sorted_dict(data, topn=1000)
    # generate wordcloud picture
#    font_path = r'C:\Windows\Fonts\simhei.ttf'
#    back_color = imread(config.bg_pic)
#    wc = wordcloud.WordCloud(font_path=font_path, mask=back_color, width=1200,height=800,min_font_size=10,max_font_size=66,max_words=1000,background_color="white")
#    wc.generate_from_frequencies(data)
#    wc.to_file(config.pic_wc_input_url_path)
    # Declare objects, render pictures
    c = (
        WordCloud()
        .add(series_name="", data_pair=data_pair, word_size_range=[10,66],word_gap=10,
             shape="cicle", width="1200", height="800",)
        .set_global_opts(
                         title_opts=opts.TitleOpts(title="WordCloud Chart\n", pos_left="center",
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=25)),
                         tooltip_opts=opts.TooltipOpts(is_show=True),
                         )
        )
    # generate wordcloud picture
    rand_filename = generate_random_filename('wordcloud', '.png')
    pic_save_path = os.path.join(config.image_dir, rand_filename)
    save_to_file(config.pic_wc_input_url_save_path, pic_save_path)
    make_snapshot(snapshot, c.render(), pic_save_path, is_remove_html=True) 
    return c
    


def wordcloud_text_by_input_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    
    # data query
    data = text_wordfreq_by_input_query()
    data_pair = get_sorted_dict(data, topn=1000)
    # generate wordcloud picture     
#    font_path = r'C:\Windows\Fonts\simhei.ttf'
#    back_color = imread(config.bg_pic)
#    wc = wordcloud.WordCloud(font_path=font_path, mask=back_color, width=1200,height=800,min_font_size=10,max_font_size=66,max_words=1000,background_color="white")
#    wc.generate_from_frequencies(data)
#    wc.to_file(config.pic_wc_input_text_path)
    # Declare objects, render pictures
    c = (
        WordCloud()
        .add(series_name="", data_pair=data_pair, word_size_range=[10,66], word_gap=8,
             shape="cicle", width="1200", height="800",is_draw_out_of_bound=False,)
        .set_global_opts(
                         title_opts=opts.TitleOpts(title="WordCloud Chart\n", pos_left="center",
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=25)),
                         tooltip_opts=opts.TooltipOpts(is_show=True),
                         )
        )
    # generate wordcloud picture                     
    rand_filename = generate_random_filename('wordcloud', '.png')
    pic_save_path = os.path.join(config.image_dir, rand_filename)
    save_to_file(config.pic_wc_input_text_save_path, pic_save_path)
    make_snapshot(snapshot, c.render(), pic_save_path, is_remove_html=True) 
    return c


def wordcloud_text_by_import_file_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    
    # data query
    data = text_wordfreq_by_import_file_query()
    data_pair = get_sorted_dict(data, topn=1000)
    # generate wordcloud picture
#    font_path = r'C:\Windows\Fonts\simhei.ttf'
#    back_color = imread(config.bg_pic)
#    wc = wordcloud.WordCloud(font_path=font_path, mask=back_color, width=1200,height=800,min_font_size=10,max_font_size=66,max_words=1000,background_color="white")
#    wc.generate_from_frequencies(data)
#    wc.to_file(config.pic_wc_input_file_path)
    # Declare objects, render pictures
    c = (
        WordCloud()
        .add(series_name="", data_pair=data_pair, word_size_range=[10,66], word_gap=8,
             shape="cicle", width="1200", height="800",is_draw_out_of_bound=False,)
        .set_global_opts(
                         title_opts=opts.TitleOpts(title="WordCloud Chart\n", pos_left="center",
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=25)),
                         tooltip_opts=opts.TooltipOpts(is_show=True),
                         )
        )
    # generate wordcloud picture                     
    rand_filename = generate_random_filename('wordcloud', '.png')
    pic_save_path = os.path.join(config.image_dir, rand_filename)
    save_to_file(config.pic_wc_input_file_save_path, pic_save_path)
    make_snapshot(snapshot, c.render(), pic_save_path, is_remove_html=True)                         
    return c



















