# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:05:07 2020

@author: Xu
"""
import __init__
from collections import defaultdict
import sys


class textrank_graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.d = 0.85 #d是阻尼系数，一般设置为0.85
        self.min_diff = 1e-5 #设定收敛阈值

    #添加节点之间的边
    def addEdge(self, start, end, weight):
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))

    #节点排序
    def rank(self):
        #一共有14个节点
        print(len(self.graph))
        #默认初始化权重
        weight_deault = 1.0 / (len(self.graph) or 1.0)
        #nodeweight_dict, 存储节点的权重
        nodeweight_dict = defaultdict(float)
        #outsum，存储节点的出度权重
        outsum_node_dict = defaultdict(float)
        #根据图中的边，更新节点权重
        for node, out_edge in self.graph.items():
            #是 [('是', '全国', 1), ('是', '调查', 1), ('是', '失业率', 1), ('是', '城镇', 1)]
            nodeweight_dict[node] = weight_deault
            outsum_node_dict[node] = sum((edge[2] for edge in out_edge), 0.0)
        #初始状态下的textrank重要性权重
        sorted_keys = sorted(self.graph.keys())
        #设定迭代次数，
        step_dict = [0]
        for step in range(1, 1000):
            for node in sorted_keys:
                s = 0
                #计算公式：(edge_weight/outsum_node_dict[edge_node])*node_weight[edge_node]
                for e in self.graph[node]:
                    s += e[2] / outsum_node_dict[e[1]] * nodeweight_dict[e[1]]
                #计算公式：(1-d) + d*s
                nodeweight_dict[node] = (1 - self.d) + self.d * s
            step_dict.append(sum(nodeweight_dict.values()))

            if abs(step_dict[step] - step_dict[step - 1]) <= self.min_diff:
                break

        #利用Z-score进行权重归一化，也称为离差标准化，是对原始数据的线性变换，使结果值映射到[0 - 1]之间。
        #先设定最大值与最小值均为系统存储的最大值和最小值
        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])
        for w in nodeweight_dict.values():
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w

        for n, w in nodeweight_dict.items():
            nodeweight_dict[n] = (w - min_rank/10.0) / (max_rank - min_rank/10.0)

        return nodeweight_dict

