# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 10:33:25 2020

@author: Xu
"""
# data prepare
import pandas as pd
import re
from src import config
import os
import numpy as np
from collections import Counter



## part 2: DATA 2 (product)
df = pd.read_excel(config.product_data_path_2)

# add column: product id 
df['product_id'] = df.index

# remove extra spaces
df['deployment'] = df['deployment'].astype(str).map(lambda x: re.sub(r'\s+','',x))
df['deployment'] = df['deployment'].map(lambda x: np.nan if x=='nan' else x)


df['training'] = df['training'].astype(str).map(lambda x: re.sub(r'\s+','',x))
df['training'] = df['training'].map(lambda x: np.nan if x=='nan' else x)

df['support'] = df['support'].astype(str).map(lambda x: re.sub(r'\s+','',x))
df['support'] = df['support'].map(lambda x: np.nan if x=='nan' else x)


# add new feature:price
# handle unclearly defined fields
import locale
locale.setlocale(locale.LC_ALL,'English_US')

df['starting_price_method'] = df['starting_price'].astype(str).map(lambda x: re.split(r'/',x,maxsplit=1)[1] if len(re.split(r'/',x,maxsplit=1))>1 else 'Not provided by vendor')
df['starting_price_num'] =  df['starting_price'].astype(str).map(lambda x: locale.atof(re.sub(r'\$', '',re.split(r'/',x,maxsplit=1)[0])) if re.match(r'^\$\S+',re.split(r'/',x,maxsplit=1)[0])!=None else float('inf'))                                                           

# missing data process:'Not provided by vendor'

import random

def get_num_by_prob(num_list, prob_list):
        x = random.uniform(0, 1)
        cum_pro = 0.0
        for num, pro in zip(num_list, prob_list):
            cum_pro += pro
            if x < cum_pro:
                return num
            
def get_num_by_prob_range(num_range_list, prob_list):
    x = random.uniform(0, 1)
    cum_pro = 0.0
    for num_range, pro in zip(num_range_list, prob_list):
        cum_pro += pro
        if x < cum_pro:
            num = np.random.uniform(num_range[0],num_range[1])
            return num
        
def get_uniform_random_num(low, high):
    num = np.random.uniform(low, high)
    return round(num,2)
        
def fill_missing_data(dist, dtype='str'):
    """
    It is used to generate random number or string based on 
    your given distribution. Here specifically refers to the frequency distribution,like:
    - dist = {'a':0.1,'b':0.2,'c':0.7}, dtype='str': return a random string,like 'c'
    - dist = {[0,10]: 0.8,[11,100]:0.2}, dtype='int':return a random integer, like 7
    - dist = {[0,10]: 0.8,[11,100]:0.2}, dtype='float':return a random decimal, like 20.5
    
    Parameters
    ----------
    dist: TYPE-dictionary
        DESCRIPTION: specifically refers tofrequency distribution. 
        The keys of the dictionary represent all possible random values,
        and the values represent the probability of obtaining each key.
        i.e. dist = {'a':0.1,'b':0.2,'c':0.7}, dist = {'a':1,'b':2,'c':7}
        If the value (frequency) is not a decimal, it is automatically converted to a decimal.
        
    dtype: TYPE-str
        DESCRIPTION: the data type of random value, default is 'str', options='str','int','float'.

    Returns
    -------
    result: Type-depends on 'dtype'
        DESCRIPTION: a random value

    """    
    num_list = list(dist.keys())
    prob_list = list(dist.values())
    if sum(prob_list)>1:
        prob_list = [sum(prob_list)-p for p in prob_list]
        prob_list = [p/sum(prob_list) for p in prob_list]
        
    if dtype=='str':
       return get_num_by_prob(num_list, prob_list)    
    elif dtype=='int':
        return int(get_num_by_prob(num_list, prob_list))
    else:
        return round(get_num_by_prob(num_list, prob_list),2)
    
# missing data process:'Not provided by vendor'
# fill the starting price method 
starting_price_method_dic = dict(Counter(df['starting_price_method']))
del starting_price_method_dic['Not provided by vendor']
df['starting_price_method_fill'] = df['starting_price_method'].map(lambda x: fill_missing_data(starting_price_method_dic, dtype='str') if x=='Not provided by vendor' else x)

# prices interval
prices_range = {}
for m in starting_price_method_dic.keys():
    price_list = list(df.loc[(df['starting_price_method']==m),'starting_price_num'].values)
    if len(price_list)>1:
        prange = [min(price_list), max(price_list)]
    else:
        prange = [price_list[0]*0.05, price_list[0]*1.5]
    prices_range[m] = prange

# fill the starting price num
import copy 

df['starting_price_num_fill'] = copy.copy(df['starting_price_num'])
for i in df.index:
    k = df.loc[i, 'starting_price_method_fill']
    if df.loc[i, 'starting_price_num_fill'] == float('inf'):
        df.loc[i, 'starting_price_num_fill'] = get_uniform_random_num(prices_range[k][0], prices_range[k][1]) 

# save new data
df.to_csv(config.product_data_path, index=False)  


# ---------------------------------------------------------------------------------

## part 1: DATA 1 (user)
data = pd.read_excel(config.user_data_path_1)
## missing data process
data['rating_overall'] = data['rating_overall'].map(lambda x: float(re.sub('/5','',x)))
data['rating_likelihood_to_recommend'] = data['rating_likelihood_to_recommend'].fillna(method='pad')
data['rating_likelihood_to_recommend'] = data['rating_likelihood_to_recommend'].map(lambda x: float(x.split('/')[0])/2)

for i in ['rating_ease_of_use','rating_customer_support','rating_value_for_money','rating_features_functionality']:
    data[i] = data[i].fillna(data[i].mode()[0])
    data[i] = data[i].map(lambda x: float(x))


## check data features 
# remove wrong field
p = re.compile(r'(\d+\-\d+ \w+)')
data['user_industry']= data['user_industry'].astype(str).map(lambda x: p.sub('nan',x))
data['user_industry'] = data['user_industry'].map(lambda x: np.nan if x=='nan' else x)

#  remove wrong field
#删除这列中错误的字段'Wellness and Fitness'
# data.index[data['user_company_size']=='Wellness and Fitness'].tolist()
data['user_company_size'].where(cond=data['user_company_size']!='Wellness and Fitness',other=np.nan,inplace=True)

# remove wrong field
data['user_job_title'] = data['user_job_title'].astype(str).map(lambda x: 'nan' if re.match(r'\W+',x)!=None else x)
data['user_job_title'] = data['user_job_title'].map(lambda x: np.nan if x=='nan' else x)

# add product id
data = pd.merge(left=data, right=df[['product_id','product_name']], how='left', on='product_name')

# save new data
data.to_csv(config.user_data_path, index=False)      




# ---------------------------------------------------------------------------------
# review data 
def get_review_data():
    """
    It is used to read data and build a specific data frame, includes
    review data items and product data items.
    
    Return
    -------
    review_data_item: type-dataframe, columns: review_id, product_name, user_name, text,
        like ['product_1', 'user_name_1', 4.5, '....'], ....
    product_data_item: type-dataframe, columns: product_id, product_name, review_count, rate
        like ['product_1', 12], ....
    
    """
    
    df = pd.read_csv(config.user_data_path)
    
    # review data
    review_data_item = df[['product_name', 'user_name', 'review_title']]
    review_data_item = review_data_item.rename(columns={'review_title':'review'}).dropna(subset=['review'])
    for col in ['software_pros', 'software_cons', 'software_overall_experience', 
                'software_comments', 'software_recommendations']:
        df1 = df[['product_name', 'user_name', col]]
        df1 = df1.rename(columns={col:'review'}).dropna(subset=['review'])
        review_data_item = pd.concat([review_data_item, df1])
        
    # product data 
    product_basic = review_data_item.groupby('product_name').count()['user_name'].reset_index(name="review_count")
    product_rate = df.groupby('product_name').mean()[['rating_overall', 'rating_ease_of_use', 
                             'rating_customer_support', 'rating_features_functionality', 
                             'rating_value_for_money', 'rating_likelihood_to_recommend']].reset_index()
    product_data_item = pd.merge(left=product_basic,right=product_rate,on='product_name')
    
    # save review data
    ReviewData = pd.merge(left = review_data_item, right = product_data_item, how='inner', on='product_name')
    ReviewData = pd.merge(left = ReviewData, right = df[['product_name','product_id']].drop_duplicates(), how='left', on='product_name')
    ReviewData.to_csv(config.review_data_path, index_label='review_id')
    
    # save product data
    df2 = pd.read_csv(config.product_data_path)
    ProductData = pd.merge(left = product_basic, right = df2[['product_name','product_id']].drop_duplicates(), how='outer', on='product_name')
    ProductData = ProductData.fillna(0)
    ProductData.to_csv(config.business_data_path, index=False)
    
get_review_data() 


















