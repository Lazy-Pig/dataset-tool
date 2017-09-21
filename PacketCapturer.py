# coding: utf-8

import pcapy
import threading
import config
import logging
from PyQt4 import QtCore
from queue import Queue
from string import digits
from random import choice
from string import ascii_uppercase
from string import ascii_lowercase


logger = logging.getLogger("log")


class PacketCapturer(threading.Thread):
    def __init__(self):
        super(PacketCapturer, self).__init__()
        self.device = config.device
        self.is_capture_enable = False
        self.queue = Queue()
        self.setDaemon(True)

    def _handle_packet(self, header, data):
        if self.is_capture_enable:
            logger.debug(QtCore.QString(u"抓到包了"))
            self.queue.put((header, data))
        else:
            pass
            # logger.debug(QtCore.QString(u"抛弃这个包"))

    def enable_capture(self):
        self.is_capture_enable = True

    def disable_capture(self):
        self.is_capture_enable = False

    def dump_packets(self, label):
        # 文件名格式： 随机生成一个长度为10的字符串_标签.pcap
        rand_name = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(10))
        file_name = 'dataset/%s_%s.pcap' % (rand_name, label)
        dumper = self.pcap.dump_open(file_name)
        logger.info(QtCore.QString(u"正在将数据包dump到 %s ..." % file_name))
        while not self.queue.empty():
            header, data = self.queue.get()
            dumper.dump(header, data)
        logger.info(QtCore.QString(u"数据包dump完成"))

    def drop_packets(self):
        # 以下写法为线程安全的
        with self.queue.mutex:
            self.queue.queue.clear()
        logger.debug(QtCore.QString(u"丢弃start到现在的所有数据包"))

    def run(self):
        self.pcap = pcapy.open_live(self.device, 1500, 0, 100)
        # pcap.setfilter("")
        self.pcap.loop(0, self._handle_packet)
