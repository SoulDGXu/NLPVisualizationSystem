# NLP可视化系统搭建

本项目将Capterra上爬取的产品和用户数据的可视化分析，文本关键信息的挖掘，用户的情感分析等集成到Web里面。在Web框架Flask中使用可视化工具pyecharts来动态展示可视化数据。

## 1. 环境配置

语言：Python3

编辑器：Anaconda(Spyder)

Web框架：Flask

数据可视化：Pyecharts

## 2. 源码结构

本项目开发过程采用前后端分离的模式，完整的源码结构如下图所示：

![项目文件目录结构](D:\Github\NLPVisualizationSystem\image\项目文件目录结构.png)

在项目NLPVisualizationSystem下，主要的文件及文件夹包括：app.py、src（exe、save、utils、data、image、background、static 和  templates）、frontend。

- app.py 是运行整个项目并发布到线上，
- exe是业务逻辑处理模块文件目录，
- data 是数据库操作脚本文件、爬取到的数据目录，
- image是项目涉及的图片文件目录，
- background是项目里词云图的默认背景文件目录，
- static 是资源文件目录，
- save是保存前端页面的输入数据的目录，
- templates 是模板文件目录，
- model是项目模块训练的模型，
- utils是帮助数据预处理，
- frontend是项目用到的前端主题样式模板。

## 3. 安装运行

运行前需要安装的python包：

| Package           | 用途说明                         | 版本   |
| ----------------- | -------------------------------- | ------ |
| pandas            | 结构化数据分析                   | 0.24.2 |
| numpy             | 科学计算                         | 1.19.4 |
| Flask             | web框架整合                      | 1.0.2  |
| pyecharts         | 数据可视化                       | 1.8.1  |
| werkzeug          | web应用工具包                    | 0.14.1 |
| collections       | python标准库，数据结构常用模块   | 内置   |
| newspaper3k       | python爬虫框架，适合抓取新闻网页 | 0.2.8  |
| imageio           | 图像处理包                       | 内置   |
| snapshot_selenium | 渲染图片                         | 0.0.2  |
| jieba             | 结巴分词                         | 0.39   |
| re                | 正则化表达                       | 内置   |
| random            | 用于生成伪随机数                 | 内置   |
| gensim            | NLP工具包                        | 3.7.3  |
| bert_embedding    | 提供BERT预训练模型及词表示       | 1.0.1  |
| nltk              | NLP工具包                        | 3.4    |
| mxnet             | MXNet深度学习框架                | 1.4.0  |
| sklearn           | 机器学习工具包                   | 0.19.2 |
|                   |                                  |        |

运行：

先解压src文件夹内的static和templateswen文件夹，找到app.py，可以直接`python app.py`运行。运行后在本地服务器启动一个 Flask 应用程序。在浏览器中输入地址：  http://127.0.0.1:5000/ 可以看到NLP可视化系统的页面，截图如下所示：

![首页](.\image\首页.png)

## 4. 前端页面设计

### 4.1 主题模板选择

本项目中，选择 Bootstrap 的主题样式模板：[Matrix Admin](https://www.matrixadmin.wrappixel.com/) 开源免费版本。Matrix Admin 分为开源版本和商业版本，开源版本的下载地址为：[http://matrixadmin.wrappixel.com/matrix-admin-package-full.zip](http://matrixadmin.wrappixel.com/matrix-admin-package-full.zip)。下载后得到matrix-admin-package-full.zip，依次解压得到matrix-admin-bt4文件。

解压顺序：

| 顺序 | 压缩包                        | 解压后                                                       |
| ---- | ----------------------------- | ------------------------------------------------------------ |
| 1    | matrix-admin-package-full.zip | matrix-admin-package-full ( matrix-admin-package.zip, matriz-admin-old.zip ) |
| 2    | matrix-admin-package.zip      | matrix-admin-package ( matrix-admin-bt4.zip, matriz-admin-old.zip ) |
| 3    | matrix-admin-bt4.zip          | matrix-admin-bt4 ( assets, dist,  html )                     |

Matrix Admin 的文件目录，共分为 3 个文件夹：asserts、dist 和 html。

- asserts 是第三方资源依赖文件目录，
- dist 存储的是页面资源文件，
- html 存储的是示例程序。

### 4.2 导航菜单设计

![导航菜单](.\image\导航菜单.png)

导航栏目前分了7块内容，有DashBoard、竞品分析、自动生成词云图、文本关键信息提取、文本情感分析、用户评价分析、用户画像。

- DashBoard：罗列一些实时数据指标。
- 竞品分析：对市场里的EDC产品做竞品分析， 分别从产品定价、安装、功能、培训等几方面进行数据分析与可视化的展示。
- 自动生成词云图：用户可以通过3种方式生成词云图，一是根据用户输入的网址来采集文本生成词云；二是根据用户输入的文本内容来生成词云；三是根据用户上传的文本文件来生成词云图。
- 文本关键信息提取：单文本分析：基于TextRank的算法的单文本摘要提取与关键词抽取。多文本分析：基于LDA的多文档主题分布探索。
- 文本分类：主要是文本分类项目，如图书分类，情感分类等。
- 用户评价情感分析：抓取用户对产品的评价数据，从评价文本中提取产品相关的aspects，归纳用户的正面和负面评价。
- 用户画像：采集使用EDC产品的用户数据，从用户所在行业、公司规模、职业等方面进行数据分析与可视化的展示。





## 5. 后台应用设计

### 5.1 服务接口设计

服务接口设计包括**页面请求接口和数据请求接**口:

- **页面请求接口**是浏览器对应的该页面的访问地址，
- **数据请求接口**对应的是图表对象的数据请求地址。

### 5.2 异常请求设计

针对常见错误和异常，设计异常提示程序。在templates文件夹，存放设计好的异常页面模板：error-403.html，error-404.html，error-405.html，error-500.html。





## 6. 运行演示

### 6.0 DashBoard

![首页](D:\Github\NLPVisualizationSystem\image\首页.png)

### 6.1 竞品分析

![竞品分析](D:\Github\NLPVisualizationSystem\image\竞品分析.gif)

### 6.2 文本预处理

#### 6.2.1 自动生成词云图

![自动生成词云](.\image\自动生成词云.gif)

#### 6.2.2 单文档分析——关键词提取
![1](.\image\文本关键信息提取1.png)

#### 6.2.3 多文档分析——主题分析

![2](.\image\文本关键信息提取2.png)

#### 6.2.4 新词挖掘

![新词挖掘](D:\Github\NLPVisualizationSystem\image\新词挖掘.png)

#### 6.2.5 文本数据增强



### 6.3 文本分类

![文本分类](D:\Github\NLPVisualizationSystem\image\文本分类.gif)



### 6.4 文本生成

![文本生成](D:\Github\NLPVisualizationSystem\image\文本生成.png)

### 6.5 用户分析

#### 6.5.1 用户画像

![用户画像分析](.\image\用户画像分析.png)

#### 6.5.2 用户评价情感分析

![用户评价情感分析](.\image\用户评价情感分析.gif)



