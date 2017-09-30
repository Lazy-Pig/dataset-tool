# coding: utf-8

import config
import logging

"""
TODO:
1.去除ACK包，FIN包，以及重传包
2.每个流中的数据包按seq排序
"""

class ThreeLengthSeriesData(object):
    """
    实现了Analyzing Android Encrypted Network Traffic to Identify User Actions中的预处理
    """
    def __init__(self, label_num=4, feature_num=1,max_value=1500):
        self.dataset_path = config.dataset_path
        self.save_ips_path = config.save_ips_path
        # 最大包长度，超过该长度的包一律视为这个长度，以方便包长度归一化
        self.max_value = max_value
        # 数据集的类别数量
        self.label_num = label_num
        #　每个包的特征数量，目前只有包长度一个特征，之后可以考虑添加特征
        self.feature_num = feature_num
        # 数据集的x
        self.data = []
        # 数据集的每个y对应的实际标签
        self.label_mean = {}
        # 数据集的y
        self.labels = []