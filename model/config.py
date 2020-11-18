# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:58:11 2020

@author: Xu
"""
import os


# main directory
cwd = r'D:\PythonJupyterNootebook\My NLP projects\My projects\NLPVisualizationSystem'  
data_dir =  os.path.join(cwd, 'data')   
image_dir =  os.path.join(cwd, 'image')
template_dir = os.path.join(cwd, 'templates')
background_dir = os.path.join(cwd, "background")
static_dir = os.path.join(cwd, "static")
run_dir = os.path.join(cwd, "run")
html_dir = os.path.join(cwd,"html")
save_dir = os.path.join(cwd, "save")
model_dir = os.path.join(cwd,'model')

   

# data path
user_data_path = os.path.join(data_dir, 'new_users_comments.csv')
product_data_path = os.path.join(data_dir, "new_proucts_details.csv")
user_data_path_1 = os.path.join(data_dir, 'users_comments.xls')
product_data_path_2 = os.path.join(data_dir, "data_out_proucts_details.xls")
#stopwords_path = os.path.join(data_dir, "stopwords.txt")
bg_pic = os.path.join(background_dir, "oval.png")

# WordCloud Generation
# save user input data
wc_input_url_path = os.path.join(save_dir, 'userurl.txt')
wc_input_text_path = os.path.join(save_dir, 'usertext.txt')
wc_input_file_save_path = os.path.join(save_dir, 'userfile.txt')
# save wordcloud picture
pic_wc_input_url_save_path = os.path.join(save_dir, 'wordcloud_from_url.txt')
pic_wc_input_text_save_path = os.path.join(save_dir, 'wordcloud_from_input_text.txt')
pic_wc_input_file_save_path = os.path.join(save_dir, 'wordcloud_from_input_file.txt')



# Text Extraction: configuration 
# KeyInfo Extraction
# data path
idf_path = os.path.join(data_dir, 'idf.txt')
token_vector_path = os.path.join(data_dir, 'token_vector.bin')
# save user input data
keyinfo_input_url_path = os.path.join(save_dir, 'keyinfo_input_url.txt')
keyinfo_input_text_path = os.path.join(save_dir, 'keyinfo_input_text.txt')
keyinfo_input_file_save_path = os.path.join(save_dir, 'keyinfo_input_file.txt')
# download text extraction result 
download_keyinfo_input_url_save_path = os.path.join(save_dir, 'keyinfo_from_url.txt')
download_keyinfo_input_text_save_path = os.path.join(save_dir, 'keyinfo_from_input_text.txt')
download_keyinfo_input_file_save_path = os.path.join(save_dir, 'keyinfo_from_input_file.txt')

# Topic CLuster
# data path
StopWords_path = os.path.join(data_dir, "stop_words_ch.txt")
# save user input data
topic_input_file_save_path = os.path.join(save_dir, 'topic_input_file.txt')
# download topic keywords result
download_topic_input_file_save_path = os.path.join(save_dir, 'topic_keywords_dist.txt')


# Review Sentiment Analysis
# data path
en_stopwords_path = os.path.join(data_dir, 'stopwords.txt')
review_data_path = os.path.join(data_dir, 'UserReviewData.csv')
business_data_path = os.path.join(data_dir, 'ProductData.csv')
glove_embedding_path = os.path.join(data_dir, 'glove.6B.100d.txt')

# model path 
svm_model_save_path = os.path.join(model_dir, 'svm_clf_model.pkl')
lr_model_save_path = os.path.join(model_dir, 'logistic_reg_clf_model.pkl')

# review summary save path
user_input_id_name_path = os.path.join(save_dir, 'user_input_product_id_name.txt')
review_summary_save_path = os.path.join(save_dir, 'review_summary.txt')











