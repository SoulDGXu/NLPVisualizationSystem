# NLP可视化系统搭建

本项目将Capterra上爬取的产品和用户数据的可视化分析，文本关键信息的挖掘，用户的情感分析等集成到Web里面。在Web框架Flask中使用可视化工具pyecharts来动态展示可视化数据。

## 1. 环境配置

语言：Python3

编辑器：Anaconda(Spyder)

Web框架：Flask

数据可视化：Pyecharts

## 2. 源码结构

本项目开发过程采用前后端分离的模式，完整的源码结构如下图所示：

![源码结构](.\image\源码结构.png)

在项目NLPVisualizationSystem下，文件夹包括：apps、data、image、background、static 和  templates。

- apps 是业务逻辑处理模块文件目录，
- data 是数据库操作脚本文件、爬取到的数据目录，
- image是项目涉及的图片文件目录，
- background是项目里词云图的默认背景文件目录，
- static 是资源文件目录，
- save是保存前端页面的输入数据的目录，
- templates 是模板文件目录，
- model是数据库查询模块文件、数据预处理模块文件目录，
- frontend是项目用到的前端主题样式模板。

## 3. 前端页面设计

### 3.1 主题模板选择

本项目中，选择 Bootstrap 的主题样式模板：[Matrix Admin](https://www.matrixadmin.wrappixel.com/) 开源免费版本。Matrix Admin 分为开源版本和商业版本，开源版本的下载地址为：[http://matrixadmin.wrappixel.com/matrix-admin-package-full.zip](http://matrixadmin.wrappixel.com/matrix-admin-package-full.zip)。下载后得到matrix-admin-package-full.zip，依次解压得到matrix-admin-bt4文件。

解压顺序：

| 顺序 | 压缩包                        | 解压后                                                       |
| ---- | ----------------------------- | ------------------------------------------------------------ |
| 1    | matrix-admin-package-full.zip | matrix-admin-package-full ( matrix-admin-package.zip, matriz-admin-old.zip ) |
| 2    | matrix-admin-package.zip      | matrix-admin-package ( matrix-admin-bt4.zip, matriz-admin-old.zip ) |
| 3    | matrix-admin-bt4.zip          | matrix-admin-bt4 ( assets, dist,  html )                     |

Matrix Admin 文件解压以后的目录结构如下图所示：

![Matrix Admin 文件目录结构](.\image\Matrix Admin 文件目录结构.png)

Matrix Admin 的文件目录，共分为 3 个文件夹：asserts、dist 和 html。

- asserts 是第三方资源依赖文件目录，
- dist 存储的是页面资源文件，
- html 存储的是示例程序。

### 3.2 导航菜单设计

![导航菜单](.\image\导航菜单.png)

导航栏目前分了7块内容，有DashBoard、竞品分析、自动生成词云图、文本关键信息提取、文本情感分析、用户评价分析、用户画像。

- DashBoard：罗列一些实时数据指标。
- 竞品分析：对市场里的EDC产品做竞品分析， 分别从产品定价、安装、功能、培训等几方面进行数据分析与可视化的展示。
- 自动生成词云图：用户可以通过3种方式生成词云图，一是根据用户输入的网址来采集文本生成词云；二是根据用户输入的文本内容来生成词云；三是根据用户上传的文本文件来生成词云图。
- 文本关键信息提取：单文本分析：基于TextRank的算法的单文本摘要提取与关键词抽取。多文本分析：基于LDA的多文档主题分布探索。
- 文本分类：
- 用户评价情感分析：抓取用户对产品的评价数据，从评价文本中提取产品相关的aspects，归纳用户的正面和负面评价。
- 用户画像：采集使用EDC产品的用户数据，从用户所在行业、公司规模、职业等方面进行数据分析与可视化的展示。





## 4. 后台应用设计

### 4.1 服务接口设计

服务接口设计包括**页面请求接口和数据请求接**口:

- **页面请求接口**是浏览器对应的该页面的访问地址，
- **数据请求接口**对应的是图表对象的数据请求地址。

### 4.2 异常请求设计

针对常见错误和异常，设计异常提示程序。在templates文件夹，存放设计好的异常页面模板：error-403.html，error-404.html，error-405.html，error-500.html。





## 5. 运行演示

### 5.1 竞品分析

![竞品分析](D:\Github\NLPVisualizationSystem\image\竞品分析.gif)

### 5.2 自动生成词云图

![自动生成词云](.\image\自动生成词云.gif)

### 5.3 文本关键信息提取
![1](.\image\文本关键信息提取1.png)

![2](.\image\文本关键信息提取2.png)


### 5.4 用户评价情感分析

![用户评价情感分析](.\image\用户评价情感分析.gif)



### 5.5 用户画像

![用户画像分析](.\image\用户画像分析.png)

### 5.6 文本分类

![文本分类](.\image\文本分类.gif)





## 6. 其他问题

### 6.1 词云图显示问题

Pyecharts词云图在前端页面不显示，问题溯源：前端页面里未加载词云图的js。这里加入以下script后可以正常显示。

```html
<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts-wordcloud.min.js"></script>
```

参考资料：https://github.com/ecomfe/echarts-wordcloud

### 6.2 Flask后台设计

如何将前端页面和后台程序进行联调？

首先是明确数据响应类型是POST还是GET。

POST需要从前端收集数据，再存放到后台数据库。一般对于前端中form标签的<input>、<textarea>、<button>等元素的value、text进行回传，需要设置method='post'，还有<input>或<button>的type='submit', action='/wordcloud_2'指向的是需要回传数据的那个页面。比如：

```html
<form id="example-form-tab2" action="/wordcloud_2" class="m-t-40" method="post">
 <div>                               
     <section>
         <label for="inputtext">输入文本</label>
         <textarea id="inputtext" name="inputtext" placeholder="请输入内容" style="width:1200px;height:400px;"></textarea>  
         <div class="border-top">
             <div class="card-body">
                 <div style="text-align:right">
                     <button type="button" class="btn btn-outline-dark" onclick="clearItem();">取消</button>
                     <button type="submit" class="btn btn-primary" onclick="" id="notify2" >生成词云</button>                                             
                 </div>                                                        
             </div>
         </div>                                                                                   
     </section>                                                                              
    </div>
</form>
```

GET是向后台请求数据，从后台数据库传递给前端的页面。一般的，一个是回传数据指标，一个数回传图表参数。比如：

```python
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
```

第一个是向前端页面传递数据，定义变量value="{{ curinput.userfile }}"，从"/download_wordcloudchart_3"回传，对应的HTML是：

```html
<form id="example-form-tab3" action="/download_wordcloudchart_3" class="m-t-40" method="post">
    <div>                               
        <section>
            <label for="loadfile">选择并上传文件</label>
            <div class="custom-file"><!-- class="custom-file-input"-->
                <input type="text"  id="loadfile"  name="loadfile" class="required form-control" readOnly="true" value="{{ curinput.userfile }}">
                <!-- <label class="custom-file-label" for="loadfile">选择文件...</label> -->
                <div class="invalid-feedback">Example invalid custom file feedback</div>
            </div>  
            <div class="border-top">
                <div class="card-body">
                    <div style="text-align:center">
                        <button type="submit" class="btn btn-primary" onclick="" id="notify3" >下载词云图</button>                                             
                    </div>                                                        
                </div>
            </div>                                                                                                                                                                                              
        </section>                                                                              
    </div>
</form>
```

第二个是回传图表的参数，需要在后台先生成需要的图表，如下：

```python
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


```

