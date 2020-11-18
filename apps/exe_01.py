# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 10:26:02 2020

@author: Xu

1.竞品分析：
负责响应数据查询请求，调用数据逻辑程序。
基于数据逻辑查询结果，业务逻辑程序组装出竞品分析数据并返回给前端页面。

"""

import numpy as np
import config
import pandas as pd
import collections 
from pyecharts.charts import Bar, Timeline, Radar, Tab, Boxplot
from pyecharts import options as opts



# 1. 竞品分析
# 数据逻辑： 
def itemcount(dictionary):
    """
    此函数用于计算字典重复的key个数 。
    
     Parameters
    ----------
    dictionary : TYPE-dict
       
    Returns
    -------
    count : TYPE-dict
        new dictionary.

    """
    count = {}  
    try:
        del dictionary[np.nan]  
    except:
        None
    for i in dictionary.keys():
        items = i.split(',')
        for j in items:
            j = j.strip()
            if j in count.keys():
                count[j] += dictionary[i]
            else:
                count[j] = dictionary[i]
    return count
     
def product_feature_query():
    """
    此函数用于返回产品功能的分组统计数据。

    Returns
    -------
    dataX: TYPE-list all product feature names.
    dataY: TYPE-list Product feature percentage(%).

    """

    # load data
    data = pd.read_csv(config.product_data_path)
    # select data
    num_product = data.shape[0]
    cates = collections.Counter(data['Category_Features'])
    cates1 = itemcount(dict(cates))
    dataX = list(cates1.keys())
    dataY = list(cates1.values())
    dataY = [round(i/num_product*100,2) for i in dataY] 
    return dataX, dataY


def product_edc_feature_query():
    """
    此函数用于获取EDC产品功能的分组统计数据。

    Returns
    -------
    dataX : TYPE-list
        EDC feature names.
    dataY : TYPE-list
        EDC feature percentage(%).

    """
    # load data
    data = pd.read_csv(config.product_data_path)
    # select data
    num_product = data.shape[0]
    cate_list = [list(j.strip() for j in i.split(',')) for i in data['Category_Features']]
    cate_list_edc = [i.index("Electronic Data Capture Features") for i in cate_list]
    feats = data['Category_Features_List']
    edc=dict(zip(list(eval(feats[0]).keys()),[0]*len(eval(feats[0]).keys())))   
    for i in range(len(feats)):
        if len(cate_list[i])==1:
            for j in dict(eval(feats[i])).keys():
                if dict(eval(feats[i]))[j]=='able':
                    edc[j]+=1
                else:
                    edc[j]=edc[j]
        else:
            for j in edc.keys():
                if list(eval(feats[i]))[cate_list_edc[i]]=='able':
                    edc[j]+=1
                else:
                    edc[j]=edc[j]
    dataX = list(edc.keys())
    dataY = list(edc.values())
    dataY = [round(i/num_product*100,2) for i in dataY]
    return dataX, dataY

    
def product_deployment_query():
    """
    此函数用于获取EDC产品安装的分组统计数据。

    Returns
    -------
    dataX : TYPE-list
        EDC deployment method names.
    dataY : TYPE-list
        each EDC deployment percentage(%).

    """
    # load data
    data = pd.read_csv(config.product_data_path)
    # select data
    num_product = data.shape[0]
    dp = collections.Counter(data['deployment'])
    dp1 = itemcount(dict(dp))
    dataX = list(dp1.keys())
    dataY = list(dp1.values())
    dataY = [round(i/num_product*100,2) for i in dataY] 
    return dataX, dataY
    
    
def product_train_query(): 
    """
    此函数用于获取EDC产品培训的分组统计数据。

    Returns
    -------
    dataX : TYPE-list
        EDC training method names.
    dataY : TYPE-list
        each EDC training percentage(%).

    
    """  
    
    # load data
    data = pd.read_csv(config.product_data_path)
    # select data
    num_product = data.shape[0]
    tr = collections.Counter(data['training'])
    tr1 = itemcount(dict(tr))
    dataX = list(tr1.keys())
    dataY = list(tr1.values())
    dataY = [round(i/num_product*100,2) for i in dataY] 
    return dataX, dataY
    
def product_support_query(): 
    """
    此函数用于获取EDC产品售后支持的分组统计数据。

    Returns
    -------
    dataX : TYPE-list
        EDC support method names.
    dataY : TYPE-list
        each EDC support percentage(%).

    
    """
    
    # load data
    data = pd.read_csv(config.product_data_path)
    # select data
    num_product = data.shape[0]
    sp = collections.Counter(data['support'])
    sp1 = itemcount(dict(sp))
    dataX = list(sp1.keys())
    dataY = list(sp1.values())
    dataY = [round(i/num_product*100,2) for i in dataY] 
    return dataX, dataY   



def product_price_query():
    """
    此函数用于获取EDC产品价格的分组统计数据。

    Returns
    -------
    dataX : TYPE-list
        EDC product pricing.
    dataY : TYPE-list
        EDC product pricing
        Data for each EDC pricing.

    """
    # load data
    data = pd.read_csv(config.product_data_path)
    # select data
    dataX = list(collections.Counter(data['starting_price_method_fill']).keys())
    dataY = []
    for m in dataX:     
        m_val = data.loc[(data['starting_price_method_fill']==m),'starting_price_num_fill'].values.tolist()
        dataY.append(m_val)
    return dataX, dataY
    
    

def product_rating_query():
    """
    It is used to get the average score of each product rating.

    Returns
    -------
    dataX : TYPE-list
        rating index: i.e. 'rating_overall', 'rating_ease_of_use'.
    products : TYPE-list
        all product names.
    list_dataY : TYPE-array
        each product's average rating score.

    """
    # load data
    data = pd.read_csv(config.user_data_path)
    # select data
    rate_overall_mean = round(data.groupby('product_name')['rating_overall'].mean(),2)
    rate_use_mean = round(data.groupby('product_name')['rating_ease_of_use'].mean(),2)
    rate_fun_mean = round(data.groupby('product_name')['rating_features_functionality'].mean(),2)
    rate_mn_mean = round(data.groupby('product_name')['rating_value_for_money'].mean(),2)
    rate_sp_mean = round(data.groupby('product_name')['rating_customer_support'].mean(),2)
    rate_rec_mean = round(data.groupby('product_name')['rating_likelihood_to_recommend'].mean(),2)
    df_rate = pd.concat([rate_overall_mean,
                         rate_use_mean,
                         rate_fun_mean,
                         rate_mn_mean,
                         rate_sp_mean,
                         rate_rec_mean],axis=1)
    dataX = list(df_rate.columns)
    products = list(df_rate.index)
    list_dataY = df_rate.values
    return dataX, products, list_dataY


def rt_index_query():
    """
    It is used to get the real-time index about the product and user analysis.
    
    Returns
    -------
    product_sum : TYPE-int
        number of products.
    edc_feature_sum : TYPE-int
        number of features of EDC product.
    user_sum : TYPE-int
        number of users participating in the survey.

    """
    # load data
    data = pd.read_csv(config.product_data_path)
    data2 = pd.read_csv(config.user_data_path)
    # select data
    product_sum = data.shape[0]
    edc_feature_sum = len(product_edc_feature_query()[0])
    user_sum = data2.shape[0]
    return product_sum, edc_feature_sum, user_sum
    


# 业务逻辑：
colorList = ['#bcd3bb', '#e88f70', '#9dc5c8', '#e1e8c8',
            '#7b7c68', '#e5b5b5', '#f0b489', '#928ea8',
            '#bda29a', '#376956', '#c3bed4', '#495a80',
            '#9966cc', '#bdb76a', '#eee8ab', '#a35015',
            '#04dd98', '#d9b3e6', '#b6c3fc','#315dbc']

def rt_index_base():
    """
    It is used to get the data of realtime index.

    Returns
    -------
    cur : TYPE-dict
        realt-time index.

    """
    product_sum, edc_feature_sum, user_sum = rt_index_query()
    cur = {"product_sum": product_sum, "edc_feature_sum": edc_feature_sum, "user_sum":user_sum}
    return cur


def hist_product_feature_base():  
    """
    此函数用于获取产品功能柱状图的参数。

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    # data query
    dataX, dataY = product_feature_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX)
        .add_yaxis("Product category",dataY,color='#4150d8')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"),
                         yaxis_opts=opts.AxisOpts(type_="value", name="Proportion of products(%)"),
                         title_opts=opts.TitleOpts(title="Distribution of different product function category"),
                         datazoom_opts=[opts.DataZoomOpts()],
                         legend_opts=opts.LegendOpts( pos_left="80%"),
                         )
        
        )
    return c
    
    

def hist_product_edc_feature_base():  
    """
    此函数用于获取产品EDC功能柱状图的参数。

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    # data query
    dataX, dataY = product_edc_feature_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX) 
        .add_yaxis("EDC Features",dataY,color='#28bf7e')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"),
                         yaxis_opts=opts.AxisOpts(type_="value", name="Proportion of products(%)"),
                         title_opts=opts.TitleOpts(title="Distribution of Electronic Data Capture Features"),
                         legend_opts=opts.LegendOpts( pos_left="80%"),
                         )
        
        )
    return c
    


def hist_product_deployment_base():  
    """
    此函数用于获取产品安装的柱状图的参数。

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    # data query
    dataX, dataY = product_deployment_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX)
        .add_yaxis("Deployment",dataY,color='#ed7c2f')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"), #name="Product Deployment Method", name_location="center", name_gap=25
                         yaxis_opts=opts.AxisOpts(type_="value", name="Proportion of products(%)"),
                         title_opts=opts.TitleOpts(title="Distribution of Product Deployment")
                         )
        
        )
    
    return c
    
   
    
def hist_product_train_base():  
    """
    此函数用于获取产品培训的柱状图的参数。

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    # data query
    dataX, dataY = product_train_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX)
        .add_yaxis("Training",dataY,color='#b6c2ff')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category", ),#name="Product Training Method", name_location="center", name_gap=25
                         yaxis_opts=opts.AxisOpts(type_="value", name="Proportion of products(%)"),
                         title_opts=opts.TitleOpts(title="Distribution of Product Training Method")
                         )
        
        )
    return c
    
def boxplot_product_price_base():
    """
    此函数用于获取产品价格的箱线图的参数。

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    # data query
    dataX, dataY = product_price_query()
    # Declare objects, render pictures
    c = Boxplot()
    c.add_xaxis(dataX)
    c.add_yaxis("Pricing",c.prepare_data(dataY))
    c.set_global_opts(title_opts=opts.TitleOpts(title="Distribution of Product Pricing", subtitle="Unit:$"))
    return c
    
    


def hist_product_support_base():  
    """
    此函数用于获取产品售后支持的柱状图的参数。

    Returns
    -------
    c : TYPE-echarts parameters
        return echarts parameters.

    """
    # data query
    dataX, dataY = product_support_query()
    # Declare objects, render pictures
    c = (
        Bar()
        .add_xaxis(dataX)
        .add_yaxis("Support",dataY,color='#f2a93b')
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category", ),#name="Product Support Method", name_location="center", name_gap=25
                         yaxis_opts=opts.AxisOpts(type_="value", name="Proportion of products(%)"),
                         title_opts=opts.TitleOpts(title="Distribution of Product Support Method")
                         )
        
        )
    
    return c
    
    


def radar_product_rating_base():
    """
    此函数用于获取产品多维评价的雷达图的参数。

    Returns
    -------
    tl : TYPE-echarts parameters
        return echarts parameters.
    """
    
    # data query
    dataX, products, list_dataY = product_rating_query()
    c_schema = []
    for i in range(len(dataX)):
        c_schema.append({"name":dataX[i],"max":5,"min":0})
        
    # Declare objects, render pictures
    tl = Timeline()
    for i in range(len(products)):
        c = (
            Radar(init_opts=opts.InitOpts(width="1280px", height="720px"))
            .add_schema(schema=c_schema,
                        splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),
                        textstyle_opts=opts.TextStyleOpts(color="#fff"),
                        )
            .add(series_name=products[i], data=[list(list_dataY[i])], 
                 linestyle_opts=opts.LineStyleOpts(color="#CD0000"),
                 )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(title_opts=opts.TitleOpts(title="Multi-dimensional analysis of product performance"),
                             legend_opts=opts.LegendOpts(pos_left="80%", pos_top="50%"))
        )
        tl.add(c, "{}".format(products[i]))
    return tl


def tab_product_base():
    """
    It is used to respond to requests for chart parameters.

    Returns
    -------
    tab : TYPE-echarts parameters
        return echarts parameters.

    """
    tab = Tab()
    tab.add(hist_product_feature_base(), "Product Module")
    tab.add(hist_product_edc_feature_base(), "EDC Feature")
    tab.add(hist_product_deployment_base(), "Product Deployment")
    tab.add(hist_product_support_base(),"Product Support")
    tab.add(hist_product_train_base(), "Product Train")
    tab.add(radar_product_rating_base(),"Product Rating")
    return tab











