import json
import pandas as pd
import nltk
import sentiment_model
from sentiment_model import SentimentModel


# 自定义打印方法
def print_format(str, a):
    print(str + '\n{0}\n'.format(a))


# review.json对应的数据类
class ReviewDataItem(object):
    def __init__(self, review_id, user_id, business_id, stars, text):
        self.review_id = review_id
        self.user_id = user_id
        self.business_id = business_id
        self.stars = stars
        self.text = text


# business.json对应的数据类
class BusinessDataItem(object):
    def __init__(self, business_id, name, review_count):
        self.business_id = business_id
        self.name = name
        self.review_count = review_count


class Business(object):
    """
    用来表示跟business相关的变量和函数
    """

    def __init__(self):
        # 初始化变量以及函数
        # self.aspect_filter = ["salsa"]
        self.aspect_filter = []
        self.dic_business_id = {}
        self.dic_business_data = {}
        print("step1 加载模型==================")
        self.sentimentModel = SentimentModel()  # 把已经训练好的模型存放在文件里，并导入进来
        print("step2 读取数据开始==================")
        self.read_data()
        print("step2 读取数据结束==================")

    def read_data(self):

        json_file_business_path = './data/business.json'
        json_file_review_path = './data/review.json'

        with open(json_file_business_path, 'r', encoding='utf-8') as fin:
            for line in fin:
                line_contents = json.loads(line)
                business_id = line_contents["business_id"]
                name = line_contents["name"]
                review_count = line_contents["review_count"]
                if review_count >= 100:
                    self.dic_business_id[business_id] = []
                    business_DataItem = BusinessDataItem(business_id, name, review_count)
                    self.dic_business_data[business_id] = business_DataItem

        with open(json_file_review_path, 'r', encoding='utf-8') as fin:
            for line in fin:
                line_contents = json.loads(line)
                business_id = line_contents["business_id"]
                if business_id in self.dic_business_id:
                    review_id = line_contents["review_id"]
                    user_id = line_contents["user_id"]
                    stars = line_contents["stars"]
                    text = line_contents["text"]
                    review_DataItem = ReviewDataItem(review_id, user_id, business_id, stars, text)
                    self.dic_business_id[business_id].append(review_DataItem)

    def aspect_based_summary(self, business_id):
        """
        返回一个business的summary. 针对于每一个aspect计算出它的正面负面情感以及TOP reviews.
        具体细节请看给定的文档。
        """

        aspects_dic = self.extract_aspects(business_id)
        # print(aspects_dic)
        business_name = self.dic_business_data[business_id].name
        # print(business_name)

        pos_aspect_dic = {}
        neg_aspect_dic = {}
        review_segment_dic = {}

        for aspect, reviews in aspects_dic.items():
            for review in reviews:
                review_text = review.text
                if review_text == None or str.strip(review_text) == '':
                    continue
                review_segment = self.get_segment(review_text, aspect, aspects_dic)
                # 粗略筛选一下
                if len(str.strip(review_segment)) > len(aspect) + 3:
                    # print(review_segment)
                    key = review.review_id + "_" + aspect
                    review_segment_dic[key] = review_segment

                    score = self.sentimentModel.predict_prob(review_segment)

                    if score > 0.75:
                        if aspect not in pos_aspect_dic:
                            pos_aspect_dic[aspect] = []
                        pos_aspect_dic[aspect].append([key, score])
                    else:
                        if aspect not in neg_aspect_dic:
                            neg_aspect_dic[aspect] = []
                        neg_aspect_dic[aspect].append([key, score])

        dic_aspect_summary = {}
        for aspect, reviews in aspects_dic.items():
            if aspect not in dic_aspect_summary:
                dic_aspect_summary[aspect] = {}

            # 算某个aspect的得分
            pos_aspect_review_nums = len(pos_aspect_dic[aspect])
            pos_aspect_total_scores = 0
            for item in pos_aspect_dic[aspect]:
                pos_aspect_total_scores += item[1]

            neg_aspect_review_nums = len(neg_aspect_dic[aspect])
            neg_aspect_total_scores = 0
            for item in neg_aspect_dic[aspect]:
                neg_aspect_total_scores += item[1]

            aspect_review_nums = pos_aspect_review_nums +neg_aspect_review_nums
            aspect_score = (pos_aspect_total_scores + neg_aspect_total_scores) / aspect_review_nums

            dic_aspect_summary[aspect]["rating"] = aspect_score

            # TOP 5 正面
            aspects_pos_sorted = sorted(pos_aspect_dic[aspect], key=lambda x: x[1], reverse=True)
            aspects_pos_contents = {}
            dic_aspect_summary[aspect]["pos"] = []
            for index, item in enumerate(aspects_pos_sorted):
                if len(dic_aspect_summary[aspect]["pos"]) >= 5:
                    break
                review_content = review_segment_dic[item[0]]
                if review_content not in aspects_pos_contents:
                    dic_aspect_summary[aspect]["pos"].append(review_content)
                    aspects_pos_contents[review_content] = None

            # TOP 5 负面
            aspects_neg_sorted = sorted(neg_aspect_dic[aspect], key=lambda x: x[1], reverse=False)
            aspects_neg_contents = {}
            dic_aspect_summary[aspect]["neg"] = []
            for index, item in enumerate(aspects_neg_sorted):
                if len(dic_aspect_summary[aspect]["neg"]) >= 5:
                    break
                review_content = review_segment_dic[item[0]]
                if review_content not in aspects_neg_contents:
                    dic_aspect_summary[aspect]["neg"].append(review_content)
                    aspects_neg_contents[review_content] = None

        all_aspect_scores = 0
        for item in dic_aspect_summary.items():
            all_aspect_scores += item[1]["rating"]

        business_rating = all_aspect_scores / len(dic_aspect_summary.items())

        return {'business_id':business_id,
            'business_name':business_name,
            'business_rating':business_rating,
            'aspect_summary':dic_aspect_summary
            }

    def get_segment(self, review_text, aspect, aspects_dic):

        if self.is_review_only_one_aspect(review_text):
            return review_text

        cur_aspect_index = review_text.index(aspect)
        cur_aspect_end_index_begin = cur_aspect_index + len(aspect)
        cur_aspect_end_index_end = cur_aspect_end_index_begin
        end_pos = len(review_text) - 1

        stop_punct_map = {c: None for c in ',.!?;'}
        relation_punct_list = ["and", "when", "but"]

        # next_aspect = self.get_next_aspect(review_text[cur_aspect_end_index_begin:end_pos])
        cur_aspect_des = self.get_cur_aspect_adj(review_text[cur_aspect_end_index_begin:end_pos])

        while cur_aspect_end_index_end <= end_pos:
            # 在标点符号处截取
            cur_str = review_text[cur_aspect_end_index_end:min(cur_aspect_end_index_end + 1, end_pos)]
            if cur_str in stop_punct_map:
                break

            # 在转移符号处截取
            cur_strs = review_text[cur_aspect_end_index_begin:cur_aspect_end_index_end]
            relation_store = ""
            for relation in relation_punct_list:
                if relation in cur_strs.lower():
                    relation_store = relation
                    break

            if relation_store != "":
                cur_aspect_end_index_end -= len(relation_store)
                break

            # 在下一个aspect截取
            # if next_aspect != None:
            # 	if next_aspect in aspects_dic and next_aspect in cur_strs:
            # 		cur_aspect_end_index_end -= len(next_aspect)
            # 		break

            # 在aspect最近的形容词截取
            if cur_aspect_des != None:
                if cur_aspect_des in cur_strs:
                    break

            cur_aspect_end_index_end += 1

        cur_aspect_end_index_end = min(cur_aspect_end_index_end, end_pos)
        return review_text[cur_aspect_index:cur_aspect_end_index_end]

    def get_next_aspect(self, text):
        tokens = nltk.word_tokenize(text)
        tag_tuples = nltk.pos_tag(tokens)
        for (word, tag) in tag_tuples:
            if tag == "NN":
                return word
        return None

    def get_cur_aspect_adj(self, text):
        tokens = nltk.word_tokenize(text)
        tag_tuples = nltk.pos_tag(tokens)
        for (word, tag) in tag_tuples:
            if tag == "JJ" or tag == "ADJ":
                return word
        return None

    def is_review_only_one_aspect(self, review_text):
        '''
        判断评论里面是否只包含一个方面
        :param review:
        :return:
        '''

        tagged_words = []
        tokens = nltk.word_tokenize(review_text)
        tag_tuples = nltk.pos_tag(tokens)
        for (word, tag) in tag_tuples:
            if tag == "NN":
                tagged_words.append(word)

        if len(tagged_words) <= 1:
            return True

        return False

    def extract_aspects(self, business_id):
        """
        从一个business的review中抽取aspects
        """

        # print("step3 extract_aspects begin==================")

        if business_id not in self.dic_business_id:
            print("business_id not exit")
            return None

        review_list = self.dic_business_id[business_id]
        aspects_dic = {}
        for review_data in review_list:
            sentence = review_data.text
            if sentence == None or str.strip(sentence) == '':
                continue
            tagged_words = []
            tokens = nltk.word_tokenize(sentence)
            tag_tuples = nltk.pos_tag(tokens)
            for (word, tag) in tag_tuples:
                if tag == "NN":
                    # token = {'word': string, 'pos': tag}
                    # tagged_words.append(word)
                    if word not in aspects_dic:
                        aspects_dic[word] = []
                    aspects_dic[word].append(review_data)

        # 对字典进行排序
        aspects_sorted = sorted(aspects_dic.items(), key=lambda x: len(x[1]), reverse=True)
        aspects_dic = {}
        for index, item in enumerate(aspects_sorted):
            if item[0] in self.aspect_filter:
                continue

            if len(aspects_dic.items()) < 5:
                aspects_dic[item[0]] = item[1]

        # print("step3 extract_aspects end==================")
        return aspects_dic
