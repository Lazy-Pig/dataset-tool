# coding: utf-8
import config
import os
import pickle
import re
import logging
import numpy as np
from scapy.all import PcapReader, wrpcap, Packet, NoPayload


class AllLengthData(object):
    """
        将每个样本表示成收到或发送的数据包长度向量
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

    # def to_raw_data(self):
    #     """
    #     将数据集中是的每一条样本用收到或发送的数据包长度表示（原始数据）
    #     """
    #     self.raw_data = []
    #     if not os.path.isdir(self.dataset_path):
    #         logging.info("数据集目录　%s　不存在" % self.dataset_path)
    #         return
    #
    #     for file_index, pcap_file in enumerate(os.listdir(self.dataset_path)):
    #         if not os.path.isfile(pcap_file):
    #             pass
    #         # 从文件名中匹配出标签，匹配从"_"到"."之间的字符串
    #         m = re.match(r"^.*\_(.*)\..*$" , pcap_file)
    #         label = m.group(1)
    #         item = []
    #         with PcapReader(self.dataset_path + "/" + pcap_file) as pcap_reader:
    #             for packet in pcap_reader:
    #                 # 遍历当前pcap文件中的每一个packet
    #                 try:
    #                     src = packet['IP'].fields['src']
    #                     dst = packet['IP'].fields['dst']
    #                     len = packet['IP'].fields['len']
    #                 except:
    #                     continue
    #                 # 不在目标ip list中的包就跳过
    #                 if (src not in self.save_ips) and (dst not in self.save_ips):
    #                     continue
    #                 # 每个流中的手机发送出的IP包长度为正，手机接收到IP包长度为负
    #                 tag = 1 if src == config.host_ip else -1
    #                 item.append(len)
    #             print item
    #         self.raw_data.append(item)
    #     logging.info("已将原始数据数据集转换为包长度序列")

    # def statistics(self):
    #     """
    #     在原始数据中统计出样本的最大长度、样本中的最大数值
    #     ＠return　(int, int)
    #     """
    #     max_len = 0
    #     max_value = 0
    #     len2count = {}
    #     value2count = {}
    #     for sample in self.raw_data:
    #         if len(sample) in len2count:
    #             len2count[len(sample)] += 1
    #         else:
    #             len2count[len(sample)] = 1
    #
    #         for value in sample:
    #             if value in value2count:
    #                 value2count[value] += 1
    #             else:
    #                 value2count[value] = 1
    #     for key in sorted(len2count.keys()):
    #         print key, len2count[key]
    #     print value2count
