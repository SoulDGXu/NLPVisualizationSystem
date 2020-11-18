# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 08:46:26 2020

@author: Xu

服务：

-竞品分析


-自动生成词云图：
1. 根据用户输入指定网址，通过采集该网址文本进行处理。
2. 根据用户输入文本字符串进行处理。
3. 根据用户输入载入本地文本进行处理，用户将所需要处理文本文件放入text文本夹中，指定文件名进行处理。


-文本关键信息提取
-文本情感分析
-用户评价分析
-用户画像



后台设计：
1. 服务接口设计
1.1 页面请求设计
1.2 数据请求设计
2. 异常请求设计


"""

import os
import config
from flask import Flask, render_template,send_from_directory
from flask import request, redirect, json, url_for
from werkzeug.utils import secure_filename

import exe_01
import exe_02
import exe_03
import exe_05
import exe_06 

app = Flask(__name__, template_folder=config.template_dir,static_folder=config.static_dir)

## =================================== 路由配置 ===================================

##############################################################################################

## Part 1 竞品分析 ++++++++++++++++++++++++++++++++++++++++++++++++++++
#01 DashBoard-数据请求
@app.route("/")
def index():
    cur = exe_01.rt_index_base()
    return render_template("index.html", curnumber=cur)


##01 DashBoard-图表请求
#@app.route('/category_chart')
#def get_product_category_chart():
#    c = exe_01.hist_product_feature_base()
#    return c.dump_options_with_quotes()
    
# --------------------------------------------------------------------------

#02 竞品分析-数据请求
@app.route("/product-module")
def hist_product_category():
    cur = exe_01.rt_index_base()
    return render_template("product_analysis.html", curnumber=cur)


#02 竞品分析-图表请求
@app.route('/category_chart')
def get_hist_product_category_chart():
    c = exe_01.hist_product_feature_base()
    return c.dump_options_with_quotes()

# --------------------------------------------------------------------------

#03 产品EDC功能-数据请求
@app.route("/edc")
def hist_product_edc():
    cur = exe_01.rt_index_base()
    return render_template("product_edc.html", curnumber=cur)


#03 产品EDC功能-图表请求
@app.route('/edc_chart')
def get_hist_product_edc_chart():
    c = exe_01.hist_product_edc_feature_base()
    return c.dump_options_with_quotes()

# --------------------------------------------------------------------------

#04 产品安装-数据请求
@app.route("/deployment")
def hist_product_deployment():
    cur = exe_01.rt_index_base()
    return render_template("product_deployment.html", curnumber=cur)


#04 产品安装-图表请求
@app.route('/deployment_chart')
def get_hist_product_deployment_chart():
    c = exe_01.hist_product_deployment_base()
    return c.dump_options_with_quotes()

# --------------------------------------------------------------------------

#05 产品培训-数据请求
@app.route("/train")
def hist_product_train():
    cur = exe_01.rt_index_base()
    return render_template("product_train.html", curnumber=cur)


#05 产品培训-图表请求
@app.route('/train_chart')
def get_hist_product_train_chart():
    c = exe_01.hist_product_train_base()
    return c.dump_options_with_quotes()

# --------------------------------------------------------------------------

#06 产品价格-数据请求
@app.route("/price")
def boxplot_product_price():
    cur = exe_01.rt_index_base()
    return render_template("product_price.html", curnumber=cur)


#06 产品价格-图表请求
@app.route('/price_chart')
def get_boxplot_product_price_chart():
    c = exe_01.boxplot_product_price_base()
    return c.dump_options_with_quotes()

# --------------------------------------------------------------------------

#07 产品多维评估-数据请求
@app.route("/rate")
def radar_product_rate():
    cur = exe_01.rt_index_base()
    return render_template("product_rate.html", curnumber=cur)


#07 产品多维评估-图表请求
@app.route('/rate_chart')
def get_radar_product_rate_chart():
    c = exe_01.radar_product_rating_base()
    return c.dump_options_with_quotes()



##############################################################################################

## Part 2 自动生成词云图 ++++++++++++++++++++++++++++++++++++++++++++++++++++
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
    
def save_to_file(filepath, content):
    f = open(filepath, 'w', encoding='utf-8') 
    f.write(content)
    f.close()

def check_url(url):
    """
    Check if the URL can be accessed normally.
    
    Open a simulated browser and visit.

    If the access is normal, the output is normal, and the error is output.

    Parameters
    ----------
    url : TYPE-str
        DESCRIPTION: the URL.

    Returns
    -------
    content : TYPE-str
        DESCRIPTION:The preprocessed news text.
    
    """
    import urllib
    import time
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')] #Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0
    url = url.replace('\n','').strip()
    try:
        opener.open(url)
        print(url + ' successfully accessed.')
        return True
    except urllib.error.HTTPError:
        print(url + ' = Error when accessing the page.')
        time.sleep(2)
    except urllib.error.URLError:
        print(url + " = Error when accessing the page.")
        time.sleep(2)
    time.sleep(0.1)
    return False
 
    

       
#01 tab1词云图构建-数据请求
@app.route("/wordcloud_1", methods=['GET'])
def text_wordcloud_home_1():
    return render_template("wc1.html")

#01 tab1词云图构建-获取前端输入数据        
@app.route('/wordcloud_1', methods=['POST'])
def get_url():
    url = request.form.get('texturl')
    try:
        if check_url(url):
            save_to_file(config.wc_input_url_path, url)
            print('add URL: ' + url)
        return redirect('/download_wordcloudchart_1')
    except:
        return  render_template("wc1.html")           
    

#01 tab1词云图生成-数据请求
@app.route('/download_wordcloudchart_1', methods=['GET'])  
def rt_url():
    cur = exe_02.rt_user_url_base()
    return  render_template("genwc1.html", curinput=cur)      
    
#01 tab1词云图生成-下载图片
@app.route('/download_wordcloudchart_1', methods=['POST'])
def download_wc_chart_1():
    file_dir, filename = exe_02.pic_rt_user_url_base()
    return send_from_directory(file_dir, filename, as_attachment=True)
  
#01 tab1词云图生成-图表请求    
@app.route('/wordcloud_chart_tab1')
def get_text_wordcloud_tab_1_chart():
    c = exe_02.wordcloud_text_by_url_base()
    return c.dump_options_with_quotes()


# --------------------------------------------------------------------------

#02 tab2词云图构建-数据请求  
@app.route("/wordcloud_2", methods=['GET'])
def text_wordcloud_home_2():
    return render_template("wc2.html")   


#02 tab2词云图构建-获取前端输入数据    
@app.route("/wordcloud_2", methods=['POST'])
def get_input_text():
    usertext = request.form.get('inputtext')
    try:
        if usertext != None:
            save_to_file(config.wc_input_text_path, usertext)
            print(usertext)
        return redirect('/download_wordcloudchart_2')
    except:
        return render_template("wc2.html") 


#02 tab2词云图生成-数据请求
@app.route('/download_wordcloudchart_2', methods=['GET'])  
def rt_input_text():
    cur = exe_02.rt_user_input_text_base()
    return  render_template("genwc2.html", curinput=cur)      
   
#02 tab2词云图生成-下载图片  
@app.route('/download_wordcloudchart_2', methods=['POST'])
def download_wc_chart_2():
    file_dir, filename = exe_02.pic_rt_user_input_text_base()
    return send_from_directory(file_dir, filename, as_attachment=True)
    
#02 tab2词云图生成-图表请求
@app.route('/wordcloud_chart_tab2')
def get_text_wordcloud_tab_2_chart():
    c = exe_02.wordcloud_text_by_input_base()
    return c.dump_options_with_quotes()



# --------------------------------------------------------------------------

#03 tab3词云图构建-数据请求
@app.route("/wordcloud_3", methods=['GET'])
def text_wordcloud_home_3():
    return render_template("wc3.html")


#03 tab3词云图构建-获取前端输入数据
@app.route('/wordcloud_3', methods=['POST'])
def get_import_file():
    userfile = request.files.get('loadfile')
    if userfile:
        filename = secure_filename(userfile.filename)
        types = ['txt', 'doc', 'docx']
        if filename.split('.')[-1] in types:
            uploadpath = os.path.join(config.save_dir, filename)
            userfile.save(uploadpath)
            save_to_file(config.wc_input_file_save_path, uploadpath)           
            print('文件上传成功')
            return redirect('/download_wordcloudchart_3')
    else:
        return render_template("wc3.html") 
    
    

#03 tab3词云图生成-数据请求
@app.route('/download_wordcloudchart_3', methods=['GET'])  
def rt_import_file():
    cur = exe_02.rt_user_import_file_base()
    return  render_template("genwc3.html", curinput=cur)          
    
#03 tab3词云图生成-下载图片
@app.route('/download_wordcloudchart_3', methods=['POST'])
def download_wc_chart_3():
    file_dir, filename = exe_02.pic_rt_user_import_file_base()
    return send_from_directory(file_dir, filename, as_attachment=True)
    
#03 tab3词云图生成-图表请求
@app.route('/wordcloud_chart_tab3')
def get_text_wordcloud_tab_3_chart():
    c = exe_02.wordcloud_text_by_import_file_base()
    return c.dump_options_with_quotes()




##############################################################################################
## Part 3 文本关键信息提取--单文本分析

#01 tab1关键信息提取构建-数据请求
@app.route("/keyinfo_1", methods=['GET'])
def keyinfo_home_1():
    return render_template("keyinfo1.html")

#01 tab1关键信息提取构建-获取前端输入数据        
@app.route('/keyinfo_1', methods=['POST'])
def get_keyinfo_url():
    url = request.form.get('texturl')
    try:
        if check_url(url):
            save_to_file(config.keyinfo_input_url_path, url)
            print('add URL: ' + url)
        return redirect('/download_keyinfo_1')
    except:
        return render_template("keyinfo1.html")           
    

#01 tab1关键信息生成-数据请求
@app.route('/download_keyinfo_1', methods=['GET'])  
def rt_keyinfo_url():
    cur = exe_03.rt_keyinfo_url_base()
    return  render_template("genkeyinfo1.html", curinput=cur)      
    
#01 tab1关键信息生成-下载输出结果
@app.route('/download_keyinfo_1', methods=['POST'])
def download_keyinfo_1():
    file_dir, filename = os.path.split(config.download_keyinfo_input_url_save_path)
    return send_from_directory(file_dir, filename, as_attachment=True)
  

# --------------------------------------------------------------------------

#02 tab2关键信息提取构建-数据请求

@app.route("/keyinfo_2", methods=['GET'])
def keyinfo_home_2():
    return render_template("keyinfo2.html")

#01 tab1关键信息提取构建-获取前端输入数据        
@app.route('/keyinfo_2', methods=['POST'])
def get_keyinfo_input_text():
    usertext = request.form.get('inputtext')
    try:
        if usertext != None:
            save_to_file(config.keyinfo_input_text_path, usertext)
            print(usertext)
        return redirect('/download_keyinfo_2')
    except:
        return render_template("keyinfo2.html")        
    

#01 tab1关键信息生成-数据请求
@app.route('/download_keyinfo_2', methods=['GET'])  
def rt_keyinfo_input_text():
    cur = exe_03.rt_keyinfo_input_text_base()
    return  render_template("genkeyinfo2.html", curinput=cur)      
    
#01 tab1关键信息生成-下载输出结果
@app.route('/download_keyinfo_2', methods=['POST'])
def download_keyinfo_2():
    file_dir, filename = os.path.split(config.download_keyinfo_input_text_save_path)
    return send_from_directory(file_dir, filename, as_attachment=True)



# --------------------------------------------------------------------------

#03 tab3关键信息提取构建-数据请求

@app.route("/keyinfo_3", methods=['GET'])
def keyinfo_home_3():
    return render_template("keyinfo3.html")

#01 tab1关键信息提取构建-获取前端输入数据        
@app.route('/keyinfo_3', methods=['POST'])
def get_keyinfo_import_file():
    userfile = request.files.get('loadfile')
    if userfile:
        filename = secure_filename(userfile.filename)
        types = ['txt', 'doc', 'docx']
        if filename.split('.')[-1] in types:
            uploadpath = os.path.join(config.save_dir, filename)
            userfile.save(uploadpath)
            save_to_file(config.keyinfo_input_file_save_path, uploadpath)           
            print('文件上传成功')
            return redirect('/download_keyinfo_3')
    else:
        return render_template("keyinfo3.html") 
    

#01 tab1关键信息生成-数据请求
@app.route('/download_keyinfo_3', methods=['GET'])  
def rt_keyinfo_import_file():
    cur = exe_03.rt_keyinfo_import_file_base()
    return  render_template("genkeyinfo3.html", curinput=cur)      
    
#01 tab1关键信息生成-下载输出结果
@app.route('/download_keyinfo_3', methods=['POST'])
def download_keyinfo_3():
    file_dir, filename = exe_03.download_rt_keyinfo_import_file_base()
    return send_from_directory(file_dir, filename, as_attachment=True)



##############################################################################################

## Part 3 文本关键信息提取--多文本分析

@app.route("/topic_1", methods=['GET'])
def topic_home_1():
    return render_template("topic1.html")

#01 tab1关键信息提取构建-获取前端输入数据        
@app.route('/topic_1', methods=['POST'])
def get_topic_import_file():
    userfile = request.files.get('loadfile')
    if userfile:
        filename = secure_filename(userfile.filename)
        types = ['txt', 'doc', 'docx','.csv']
        if filename.split('.')[-1] in types:
            uploadpath = os.path.join(config.save_dir, filename)
            userfile.save(uploadpath)
            save_to_file(config.topic_input_file_save_path, uploadpath)           
            print('文件上传成功')
            return redirect('/download_topic_1')
    else:
        return render_template("topic1.html") 
    

#01 tab1关键信息生成-数据请求
@app.route('/download_topic_1', methods=['GET'])  
def rt_topic_import_file():
    cur = exe_03.rt_topic_import_file_base()
    return  render_template("gentopic1.html", curinput=cur)      
    
#01 tab1关键信息生成-下载输出结果
@app.route('/download_topic_1', methods=['POST'])
def download_topic_1():
    file_dir, filename = os.path.split(config.download_topic_input_file_save_path)
    return send_from_directory(file_dir, filename, as_attachment=True)


@app.route("/topic_2")
def topic_home_2():
    return render_template("topic2.html")

##############################################################################################

## Part 4 文本分类
@app.route("/classification_1")
def book_classification_home(): 
    return render_template("text_classification1.html")
    

@app.route("/classification_2")
def sentiment_classification_home(): 
    return render_template("text_classification2.html")


@app.route("/classification_3")
def other_classification_home(): 
    return render_template("text_classification3.html")

##############################################################################################

## Part 5 用户评价情感分析
@app.route("/review", methods=['GET'])
def user_review_home():
    cur = exe_05.rt_index_base()
    return render_template("user_review.html", curnumber=cur)

# 获取前端输入数据        
@app.route('/review', methods=['POST'])
def get_user_input():
    usertext = request.form.get('name')
    try:
        if usertext != None:
            save_to_file(config.user_input_id_name_path, usertext)
            print(usertext)
        return redirect('/download_review_summary')
    except:
        return render_template("user_review.html") 
    

# 提取评论-数据请求
@app.route('/download_review_summary', methods=['GET'])  
def review_summary():
    cur = exe_05.review_summary_base()
    curnumber = exe_05.rt_index_base()
    return  render_template("genreview_result.html", curinput=cur, curnumber=curnumber)      
    
# 提取评论-下载输出结果
@app.route('/download_review_summary', methods=['POST'])
def download_review_summary():
    file_dir, filename = exe_05.download_review_summary_base()
    return send_from_directory(file_dir, filename, as_attachment=True)



##############################################################################################
    
## Part 6 用户画像
@app.route('/user')
def get_user():
    return render_template("user_profile.html")

@app.route('/user_industry_chart')
def get_user_industry_chart():
    c = exe_06.hist_user_industry_base()
    return c.dump_options_with_quotes()

@app.route('/user_company_chart')
def get_user_company_chart():
    c = exe_06.hist_user_company_size_base()
    return c.dump_options_with_quotes()

@app.route('/use_time_chart')
def get_user_product_use_time_chart():
    c = exe_06.hist_user_product_use_time_base()
    return c.dump_options_with_quotes()

@app.route('/user_job_chart')
def get_user_job_chart():
    c = exe_06.wordcloud_user_job_base()
    return c.dump_options_with_quotes()




# #############################  异常处理  ###########################
# 403错误
@app.errorhandler(403)
def miss(e):
    return render_template('error-403.html'), 403


# 404错误
@app.errorhandler(404)
def error404(e):
    return render_template('error-404.html'), 404


# 405错误
@app.errorhandler(405)
def erro405r(e):
    return render_template('error-405.html'), 405


# 500错误
@app.errorhandler(500)
def error500(e):
    return render_template('error-500.html'), 500




# 主函数
if __name__ == "__main__":
    app.run()   









