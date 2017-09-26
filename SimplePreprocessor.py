# coding: utf-8
import os
import logging
import pickle
import re
from scapy.all import PcapReader, wrpcap, Packet, NoPayload
"""
TODO:
1.去除ACK包，FIN包，以及重传包
2.每个流中的数据包按seq排序
"""

HOSTIP = '10.42.0.166'

class SimplePreprocessor(object):
    """
    实现了Analyzing Android Encrypted Network Traffic to Identify User Actions中的预处理
    """
    def __init__(self, dataset_dir="dataset", save_ips_path='weibo_out/save_ips.pkl'):
        self.dataset_path = dataset_dir
        self.save_ips_path = save_ips_path
        # processed_dataset的每一个元素代表一条样本，每个样本都是一个list，list的最后一个元素是标签
        # 每个样本包含n个tuple，一个tuple对应一条流，每个tuple含有3个list。
        # 每个样本格式如下:
        # [([发送与接收的数据包长度]，[发送的数据包长度]，[接收的数据包长度])...]
        self.processed_dataset = []
        self._load_ips()

    def _load_ips(self):
        """
        把过滤留下的ip加载进来
        """
        with open(self.save_ips_path, 'r') as f:
            self.save_ips = pickle.load(f)

    def represent_by_length(self):
        """
        将数据集中是的每一条样本用收到或发送的数据包长度表示
        """
        if not os.path.isdir(self.dataset_path):
            logging.info("数据集目录　%s　不存在" % self.dataset_path)
            return

        for file_index, pcap_file in enumerate(os.listdir(self.dataset_path)):
            if not os.path.isfile(pcap_file):
                pass
            # 从文件名中匹配出标签，匹配从"_"到"."之间的字符串
            m = re.match(r"^.*\_(.*)\..*$" , pcap_file)
            label = m.group(1)
            port2tuple = {}
            with PcapReader(self.dataset_path + "/" + pcap_file) as pcap_reader:
                for packet in pcap_reader:
                    # 遍历当前pcap文件中的每一个packet
                    try:
                        src = packet['IP'].fields['src']
                        dst = packet['IP'].fields['dst']
                        len = packet['IP'].fields['len']
                    except:
                        continue
                    try:
                        sport = packet['TCP'].fields['sport']
                        dport = packet['TCP'].fields['dport']
                    except:
                        continue
                    if (src in self.save_ips) or (dst in self.save_ips):
                        # 以手机的端口号来区分一个动作所产生的不同流，
                        # 每个流中的手机发送出的IP包长度为正，手机接收到IP包长度为负
                        port, tag = (sport, 1) if src == HOSTIP else (dport, -1)
                        # port2tuple的键是端口号，值是一个含有３个list的tuple，
                        # 第一个是发送和接收到数据包长度，第二个是发送的数据包长度，第三个是接收的数据包长度
                        if port in port2tuple:
                            port2tuple[port][0].append(tag * len)
                        else:
                            port2tuple[port] = ([tag * len], [], [])
                        if tag == 1:
                            port2tuple[port][1].append(len)
                        elif tag == -1:
                            port2tuple[port][2].append(len)
                        else:
                            raise Exception("既不是发送出去的包也不是接收到的包")
            temp = port2tuple.values()
            # 为了让每个样本的标签不同，所以在标签后面加一个文件编号（由于接下来会把所有样本的所有流进行聚类）
            temp.append(label + str(file_index))
            self.processed_dataset.append(temp)
        logging.info("已将数据集转换为包长度序列")


def main():
    preprocessor = SimplePreprocessor()
    preprocessor.represent_by_length()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s',
                        datefmt='%m-%d %H:%M')
    main()