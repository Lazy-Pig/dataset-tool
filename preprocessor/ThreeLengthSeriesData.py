# coding: utf-8

import config
import logging
import pickle
import os
import re
import numpy as np
from scapy.all import PcapReader


"""
TODO:
1.去除ACK包，FIN包，以及重传包
2.每个流中的数据包按seq排序
3.动作产生的每个流的长度没有限制
"""


class ThreeLengthSeriesData(object):
    """
    实现了Analyzing Android Encrypted Network Traffic to Identify User Actions中的预处理

    例如：
    [[[15, -10, -20], [15], [10, 20]], [[-10, 25, -10, 10], [10, 10], [25, 10]]] [0, 1]

    表示：
    第２个动作产生了两条流，第一条流先发送了长度为15的包，又收到长度为10的包，然后又收到长度为20的包
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
        # 下次从第几个样本开始拿batch
        self.batch_id = 0

        self.init()

    def init(self):
        self._load_ips()
        self.generate_dataset()

    def get_obersorvation(self):
        """
        供外部拿到与数据集相关的shape
        @return (int, int) ，每个样本中元素的特征数量，标签种类数量
        """
        return self.feature_num, self.label_num

    def _load_ips(self):
        """
        把过滤留下的ip加载进来
        """
        with open(self.save_ips_path, 'r') as f:
            self.save_ips = pickle.load(f)

    def generate_dataset(self):
        """
        解析每个pcap包，将每个样本用list形式表示
        list每个元素是list，表示动作产生的流
        每个流包含3个list，分别表示输出和输入的包长度、输出包长度和输入包长度
        """
        label_index = 0
        if not os.path.isdir(self.dataset_path):
            logging.info("数据集目录　%s　不存在" % self.dataset_path)
            return

        for pcap_file in os.listdir(self.dataset_path):
            seq_len = 0
            label = np.zeros(self.label_num)

            if not os.path.isfile(pcap_file):
                pass
            # 从文件名中匹配出标签，匹配从"_"到"."之间的字符串
            m = re.match(r"^.*\_(.*)\..*$" , pcap_file)
            raw_label = m.group(1)
            # 当出现一个还没有编号的label则给label编号
            if raw_label not in self.label_mean:
                if len(self.label_mean) >= self.label_num:
                    raise Exception("Label number error")
                self.label_mean[raw_label] = label_index
                label_index += 1
            label[self.label_mean[raw_label]] = 1
            self.labels.append(label)

            #　每个样本包含n个流，每个流用端口号来区分，每个流有3个时间序列
            sample = []
            # 端口号映射到sample list中的index
            port2index = {}
            with PcapReader(self.dataset_path + "/" + pcap_file) as pcap_reader:
                for packet in pcap_reader:
                    # 拿不到IP部分或者TCP部分的包就跳过
                    try:
                        src = packet['IP'].fields['src']
                        dst = packet['IP'].fields['dst']
                        ip_len = packet['IP'].fields['len']
                        # 包长度归一化
                        if ip_len > self.max_value:
                            ip_len = 1.0
                        else:
                            ip_len = float(ip_len) / self.max_value
                    except:
                        continue
                    try:
                        sport = packet['TCP'].fields['sport']
                        dport = packet['TCP'].fields['dport']
                    except:
                        continue
                    # 不在目标ip list中的ip就跳过
                    if (src not in self.save_ips) and (dst not in self.save_ips):
                        continue
                    port, tag = (sport, 1) if src == config.host_ip else (dport, -1)
                    if port in port2index:
                        sample[port2index[port]][0].append(tag * ip_len)
                    else:
                        # port2index中新增一个映射,port2index的length正好是下一个index
                        port2index[port] = len(port2index)
                        # 当前的这个样本新增一个流
                        sample.append([[tag * ip_len], [], []])
                    #　如果是发送出去的包则加到第二个serie中
                    if tag == 1:
                        sample[port2index[port]][1].append(ip_len)
                    # 如果是收到的包则加到第三个serie中
                    elif tag == -1:
                        sample[port2index[port]][2].append(ip_len)
                    else:
                        raise Exception("既不是发送出去的包又不是接收到的包，所以你是一个什么包")
            self.data.append(sample)
        logging.info("已将数据集转换为包长度序列")

    def next(self, batch_size=1):
        """
        返回一个batch的数据，直到拿到数据集的最后一批样本则再从头开始
        ＠param batch_size　int 批的大小
        ＠return (list, list, list) 一个batch的ｘ, 一个batch的labels，一个batch的样本的长度
        @notice　ThreeLengthSeriesData一般情况下batch size应该是１
        """
        if batch_size != 1:
            raise Exception("这个数据集的batch size最好为１")

        if self.batch_id == len(self.data):
            self.batch_id = 0
        batch_data = (self.data[self.batch_id:min(self.batch_id + batch_size, len(self.data))])
        batch_labels = (self.labels[self.batch_id:min(self.batch_id + batch_size, len(self.data))])
        self.batch_id = min(self.batch_id + batch_size, len(self.data))
        return batch_data, batch_labels