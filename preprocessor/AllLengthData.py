# coding: utf-8
import config
import os
import pickle
import re
import logging
import numpy as np
from scapy.all import PcapReader


class AllLengthData(object):
    """
    将每个样本表示成收到或发送的数据包长度向量。

    例如：
    一个动作共产生了3个包，发送一个长度为20的包，接着收到一个长度为10的包，然后又收到一个长度为30的包，
    则原始数据表达为：　
        [[20],[-10],[30]] 标签为　动作0
    经过归一化，填充到固定长度，标签one hot encoding后，最终数据表达为:
        [[0.013], [-0.0065], [0.0195], 0, 0] [1, 0]
        （归一化将每一个元素除以1500；填充至长度为5；一共有２种动作）
    """
    def __init__(self, label_num=4, max_len=200, max_value=1500):
        self.dataset_path = config.dataset_path
        self.save_ips_path = config.save_ips_path
        # 样本的最大长度
        self.max_len = max_len
        # 样本的最大值
        self.max_value = max_value
        # 数据集的类别数量
        self.label_num = label_num
        # 数据集的x
        self.data = []
        # 数据集的每个y对应的实际标签
        self.label_mean = {}
        # 数据集的y
        self.labels = []
        # 每个样本的长度
        self.samples_len = []
        # 下次从第几个样本开始拿batch
        self.batch_id = 0

    def init(self):
        self._load_ips()
        self.generate_dataset()

    def _load_ips(self):
        """
        把过滤留下的ip加载进来
        """
        with open(self.save_ips_path, 'r') as f:
            self.save_ips = pickle.load(f)

    def generate_dataset(self):
        """
        解析每个pcap包，将每个样本用向量形式表示，向量每个元素是每个包长度。
        """
        label_index = 0
        if not os.path.isdir(self.dataset_path):
            logging.info("数据集目录　%s　不存在" % self.dataset_path)
            return

        for pcap_file in os.listdir(self.dataset_path):
            seq_len = 0
            label = np.zeros(self.label_num)
            sample = np.zeros((self.max_len, 1))

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

            with PcapReader(self.dataset_path + "/" + pcap_file) as pcap_reader:
                for packet in pcap_reader:
                    # 舍弃max_len以后的包
                    if seq_len > self.max_len - 1:
                        break
                    # 拿不到IP部分的包就跳过
                    try:
                        src = packet['IP'].fields['src']
                        dst = packet['IP'].fields['dst']
                        ip_len = packet['IP'].fields['len']
                    except:
                        continue
                    # 不在目标ip list中的ip就跳过
                    if (src not in self.save_ips) and (dst not in self.save_ips):
                        continue
                    # 每个流中的手机发送出的IP包长度为正，手机接收到IP包长度为负
                    tag = 1 if src == config.host_ip else -1
                    # 将ip_len归一化
                    if ip_len > self.max_value:
                        sample[seq_len] = (1.0 * tag)
                    else:
                        sample[seq_len] = (float(ip_len) / self.max_value) * tag
                    seq_len += 1
                self.samples_len.append(seq_len)
            self.data.append(sample)
        logging.info("已将数据集转换为包长度序列")

    def next(self, batch_size):
        """
        返回一个batch的数据，直到拿到数据集的最后一批样本则再从头开始
        ＠param batch_size　int 批的大小
        ＠return (list, list, list) 一个batch的ｘ, 一个batch的labels，一个batch的样本的长度
        """
        if self.batch_id == len(self.data):
            self.batch_id = 0
        batch_data = (self.data[self.batch_id:min(self.batch_id + batch_size, len(self.data))])
        batch_labels = (self.labels[self.batch_id:min(self.batch_id + batch_size, len(self.data))])
        batch_seqlen = (self.samples_len[self.batch_id:min(self.batch_id + batch_size, len(self.data))])
        self.batch_id = min(self.batch_id + batch_size, len(self.data))
        return batch_data, batch_labels, batch_seqlen
