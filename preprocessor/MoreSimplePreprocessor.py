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

class MoreSimplePreprocessor(object):
    """
    将每个样本表示成收到或发送的数据包长度向量
    """
    def __init__(self, dataset_dir="../dataset", save_ips_path='../weibo_out/save_ips.pkl'):
        self.dataset_path = dataset_dir
        self.save_ips_path = save_ips_path
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
            lens = []
            with PcapReader(self.dataset_path + "/" + pcap_file) as pcap_reader:
                for packet in pcap_reader:
                    # 遍历当前pcap文件中的每一个packet
                    try:
                        src = packet['IP'].fields['src']
                        dst = packet['IP'].fields['dst']
                        len = packet['IP'].fields['len']
                    except:
                        continue

                    if (src not in self.save_ips) and (dst not in self.save_ips):
                        continue
                    # 每个流中的手机发送出的IP包长度为正，手机接收到IP包长度为负
                    tag = 1 if src == HOSTIP else -1
                    lens.append(tag * len)
            lens.append(label)
            print lens
        logging.info("已将数据集转换为包长度序列")


def main():
    preprocessor = MoreSimplePreprocessor()
    preprocessor.represent_by_length()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s',
                        datefmt='%m-%d %H:%M')
    main()