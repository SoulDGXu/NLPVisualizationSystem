# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:24:59 2020

@author: Xu

项目介绍：自动词云生成
对给定的文本进行关键词和高频词统计并根据指定图片形状来生成词云图。


项目功能：
三种类型的高频词和关键词可视化：
1. 根据用户输入指定网址，通过采集该网址文本进行处理。
2. 根据用户输入文本字符串进行处理。
3. 根据用户输入载入本地文本进行处理，用户将所需要处理文本文件放入text文本夹中，指定文件名进行处理。


项目实现：
主要通过调用wordcloud这个可视化组件来完成任务。

输入用户给定参数:
1) textfile: 放于text文件夹中, 为用户需要分析的文本
2) picturefile: 放于background文件夹中, 为用户给定的图片源文件
3) url: 用户需要进行分析网页文本的url
4) content: 用户需要分析的文本字符串
5) save_name: 用户对当前分析目标的命名
6) word_num: 用户希望展示的词数

输出: 在output文件夹下会生成以save_name开头的高频词云图和关键词云图

"""


import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from compute_keywords_tfidf import *
from collections import Counter
from jieba import posseg 
import urllib.request
from wordcloud import WordCloud, ImageColorGenerator
from newspaper import Article


class CreateWordCloud:
    def __init__(self):
        cur = 'D:\\NLP\\My projects\\Capterra信息提取\\Key Info Extraction'
        self.textdir = os.path.join(cur, 'text')
        self.background = os.path.join(cur, 'background')
        self.fontpath = os.path.join(cur, 'data\\simhei.ttf')
        self.outpath = os.path.join(cur, 'output')
        self.pos_filters = ['n', 'v', 'a']
        self.limit_words = 100
        self.Keyworder =  TFIDF()
        return

    '''获取搜索页'''
    def get_html(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        return html

    '''读取本地文件进行处理'''
    def read_local_file(self, textfile):
        textpath = os.path.join(self.textdir, textfile)
        content = open(textpath,'r',encoding='utf-8').read()
        return content

    '''统计词频'''
    def extract_words(self, content):
        words = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            words += [w.word for w in posseg.cut(line) if w.flag[0] in self.pos_filters and len(w.word) > 1]
        word_dict = {i[0]: i[1] for i in Counter(words).most_common()}
        return word_dict

    '''抽取关键词'''
    def extract_keywords(self, content, words_num=20):
        keywords_dict = {}
        keywords = self.Keyworder.extract_keywords(content, words_num)
        for key in keywords:
            word = key[0]
            value = int(key[1]*1000)
            keywords_dict[word] = value
        return keywords_dict

    '''创建关键词云图'''
    def show_cloud(self, word_dict, max_words, picturefile, save_name):
        self.backimage = os.path.join(self.background, picturefile)
        saveimage = os.path.join(self.outpath, save_name + '.jpg')
        backgroud_Image = np.array(Image.open(self.backimage))
        plt.figure(figsize=(15,10))
        cloud = WordCloud(font_path=self.fontpath,
                          background_color='white',
#                          width=800,
#                          height=600,
                          max_words= max_words,
                          max_font_size=500,
                          mask=backgroud_Image,
                          random_state=50
                          )

        word_cloud = cloud.generate_from_frequencies(word_dict)
#        img_colors = ImageColorGenerator(backgroud_Image)
#        word_cloud.recolor(color_func=img_colors)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.savefig(saveimage)
        # plt.show()
        # plt.close()



    '''展示关键词云图'''
    def show_keywords(self, content, picturefile, words_num=20, save_name = 'test'):
        keywords_text = self.extract_keywords(content, words_num)
        self.show_cloud(keywords_text, words_num, picturefile, save_name)
        return

    '''展示高频词云图'''
    def show_topwords(self, content, picturefile, words_num=50, save_name = 'test'):
        topwords_text = self.extract_words(content)
        self.show_cloud(topwords_text, words_num, picturefile, save_name)
        return

    '''在线模式抓取新闻进行既定形状可视化'''
    def get_webcontent(self, url):
        news = Article(url, language='zh')
        news.download()
        news.parse()
        content = news.text
        return content

    
    '''根据用户输入url进行处理'''
    def show_wordcloud_online(self, url, picturefile, words_num, save_name):
        content = self.get_webcontent(url)
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''根据用户输入文本进行处理'''
    def show_wordcloud_input(self, content, picturefile, words_num, save_name):
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''根据用户输入载入本地文本进行处理'''
    def show_wordcloud_offline(self, textfile, picturefile, words_num, save_name):
        content = self.read_local_file(textfile)
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''分别执行绘制关键词和高频词'''
    def show_main(self, content, picturefile, words_num, save_name):
        name = save_name + '-topwords'
        print('正在生成该文本的高频词云图.....')
        self.show_topwords(content, picturefile, words_num, name)
        print('已完成该文本的高频词云图.....')
        print('正在生成该文本的关键词云图.....')
        name = save_name + '-keywords'
        self.show_keywords(content, picturefile, words_num, name)
        print('已完成该文本的关键词云图.....')

def test():
    print('*'*10 +'根据输入文本进行处理：'+ '*'*10)
    with open('text\\test_article.txt', 'r', encoding='utf-8') as f:
        content = f.readlines()[0]
        print(content[:100]+'...')
        picturefile = 'china.jpg'
        save_name = 'test'
        words_num = 50
        handler = CreateWordCloud()
        handler.show_wordcloud_input(content, picturefile, words_num, save_name)
    f.close()
    
    print('*'*10 +'根据输入url进行处理：'+ '*'*10)
    with open('text\\test_url.txt', 'r', encoding='utf-8') as f1:
        url = f1.readlines()[-1].strip()
        print(url)
        picturefile = 'oval.png'
        save_name = 'test1'
        words_num = 50
        handler = CreateWordCloud()
        handler.show_wordcloud_online(url, picturefile, words_num, save_name)
    f1.close()
    
    print('*'*10 +'根据输入载入本地文本进行处理：'+ '*'*10)
    textfile = 'test_article.txt'
    picturefile = 'profile.png'
    save_name = 'test2'
    words_num = 50
    handler = CreateWordCloud()
    print('load text file from {}'.format(os.path.join(handler.textdir, textfile)))
    handler.show_wordcloud_offline(textfile, picturefile, words_num, save_name)
    
    
    

if __name__ == '__main__':
    test()

