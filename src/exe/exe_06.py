# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 09:20:06 2020

@author: Xu

6.用户画像

负责响应数据查询请求，调用数据逻辑程序。
基于数据逻辑查询结果，业务逻辑程序组装出用户画像数据并返回给前端页面。

"""


import __init__
import re
import os
import pandas as pd
import numpy as np
import collections 
from src import config
from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, Page, Tab

# 6. 用户画像分析
# 数据逻辑： 
def user_industry_query():
    """
    It is used for data query of user industry. 

    Returns
    -------
    dataX : TYPE-list
        DESCRIPTION:all user industry choices.
    dataY : TYPE-list
        DESCRIPTION:number of users in different industries.

    """
    # load data
    data = pd.read_csv(config.user_data_path)
    # select data
    dataX = list(collections.Counter(data['user_industry']).keys())
    dataY = list(collections.Counter(data['user_industry']).values())
    remove_nan_indx = dataX.index(np.nan)
    dataX.remove(np.nan)
    dataY.pop(remove_nan_indx)
    return dataX,dataY


def user_product_use_time_query():
    """
    It is used for data query of how long users use the product. 

    Returns
    -------
    dataX : TYPE-list
        DESCRIPTION:all product use time choices.
    dataY : TYPE-list
        DESCRIPTION:number of users in different usage time.

    """
    # load data
    data = pd.read_csv(config.user_data_path)
    # select data
    dataX = list(collections.Counter(data['used_years']).keys())
    dataY = list(collections.Counter(data['used_years']).values())
    remove_nan_indx = dataX.index(np.nan)
    dataX.remove(np.nan)
    dataY.pop(remove_nan_indx)
    return dataX,dataY


def user_company_size_query():
    """
    It is used for data query of user company size. 

    Returns
    -------
    dataX : TYPE-list
        DESCRIPTION:all company size.
    dataY : TYPE-list
        DESCRIPTION:number of users in different companies.

    """
    # load data
    data = pd.read_csv(config.user_data_path)
    # select data
    dataX = list(collections.Counter(data['user_company_size']).keys())
    dataY = list(collections.Counter(data['user_company_size']).values())
    remove_nan_indx = dataX.index(np.nan)
    dataX.remove(np.nan)
    dataY.pop(remove_nan_indx)
    return dataX,dataY



def user_job_query():
    """
    It is used for data query of user job title. 

    Returns
    -------
    dataX : TYPE-list
        DESCRIPTION:all jobs.
    dataY : TYPE-list
        DESCRIPTION:number of users in different jobs.

    """
    # load data
    data = pd.read_csv(config.user_data_path)
    # select data
    dataX = list(collections.Counter(data['user_job_title']).keys())
    dataY = list(collections.Counter(data['user_job_title']).values())
    remove_nan_indx = dataX.index(np.nan)
    dataX.remove(np.nan)
    dataY.pop(remove_nan_indx)
    return dataX,dataY

def user_job_wordcloud_freq_query():
    """
    It is used to count the frequency of words for user job title.

    Returns
    -------
    data_pair : TYPE-list(tuple)
        DESCRIPTION: Count the frequency of words,like [(word1, count1), (word2, count2),...].

    """
    
    # load data
    dataX, dataY = user_job_query()
    # select data
    token = [ re.split(r'\W+',job) for job in dataX]
    vocab = {}
    for i in range(len(token)):
        for word in token[i]:
            if word not in vocab:
                vocab[word] = dataY[i]
            else:
                vocab[word] += dataY[i]
    data_pair = list(vocab.items())
    return data_pair
        
    

# 业务逻辑：
def hist_user_industry_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    
    # data query
    dataX, dataY = user_industry_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX)
        .add_yaxis("Industry", dataY,color='#b6c2ff')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"),
                         yaxis_opts=opts.AxisOpts(type_="value", name="number of users"),
                         title_opts=opts.TitleOpts(title="User Industry Distribution",pos_left="center"), 
                         legend_opts=opts.LegendOpts(pos_left="80%",),                                              
                         datazoom_opts=[opts.DataZoomOpts()],
                         )
        
        )
    return c
    

def hist_user_company_size_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    
    # data query
    dataX, dataY = user_company_size_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX)
        .add_yaxis("Company Size", dataY, color='#ed7c2f')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"),
                         yaxis_opts=opts.AxisOpts(type_="value", name="number of users"),
                         title_opts=opts.TitleOpts(title="User Company Size Distribution", pos_left="center"), 
                         legend_opts=opts.LegendOpts(pos_left="70%",pos_top="5%"),                                                                          
                         )
        
        )
    return c
 
   
def hist_user_product_use_time_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    
    # data query
    dataX, dataY = user_product_use_time_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX)
        .add_yaxis("Product Usage Time", dataY, color='#28bf7e')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"),
                         yaxis_opts=opts.AxisOpts(type_="value", name="number of users"),
                         title_opts=opts.TitleOpts(title="Distribution of cumulative product usage time by users",pos_left="center"),                                                                      
                         legend_opts=opts.LegendOpts(pos_left="70%",pos_top="5%"),
                         )
        
        )
    return c

def wordcloud_user_job_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    
    # data query
    data_pair = user_job_wordcloud_freq_query()
    # Declare objects, render pictures
    c = (
        WordCloud()
        .add(series_name="Occupation", data_pair=data_pair, word_size_range=[10,100],
             shape="cicle", width="1200", height="800",)
        .set_global_opts(
                         title_opts=opts.TitleOpts(title="User Occupation Analysis", pos_left="center",
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
                         tooltip_opts=opts.TooltipOpts(is_show=True),
                         )
        )
    return c


def pic_wordcloud_user_jov_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    image : TYPE-IMAGE Component parameters
        DESCRIPTION:IMAGE html parameters.

    """
    
    # get picture
    from wordcloud import WordCloud
    
    data_pair = user_job_wordcloud_freq_query()
    wc = WordCloud(width=1200,height=800,min_font_size=10,max_font_size=100,font_step=2,max_words=10000,background_color="white")
    wc.generate_from_frequencies(dict(data_pair))
    wc.to_file(os.path.join(config.image_dir,"wordcloud_user_job.png"))
    # render picture
    from pyecharts.components import Image
    from pyecharts.options import ComponentTitleOpts
    
    image = Image()
    img_src = (os.path.join(config.image_dir,"wordcloud_user_job.png"))
    image.add(src=img_src,
              style_opts={"width": "1200px", "height": "800px", "style": "margin-top: 20px"},
              )
    image.set_global_opts(title_opts=ComponentTitleOpts(title="User Occupation Analysis"))
    return image



def page_user_analysis_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    page : TYPE-echarts parameters
        return echarts parameters.

    """
    page = Page(interval=10, layout=Page.SimplePageLayout)
    page.add(
        hist_user_industry_base(),
        hist_user_company_size_base(),
        hist_user_product_use_time_base(),
        wordcloud_user_job_base(),
        ) 
    return page


def tab_user_analysis_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    tab : TYPE-echarts parameters
        return echarts parameters.

    """
    tab = Tab()
    tab.add(hist_user_industry_base(), "User Industry")
    tab.add(hist_user_company_size_base(), "User Company")
    tab.add(hist_user_product_use_time_base(), "Product Usage Time")
    tab.add(wordcloud_user_job_base(), "User Occupation")
    return tab
    

