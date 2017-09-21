# coding: utf-8

import pcapy
import threading
import config
import logging
from PyQt4 import QtCore
from queue import Queue


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

    def dump_packets(self):
        dumper = self.pcap.dump_open('result.pcap')
        logger.info(QtCore.QString(u"正在dump数据包..."))
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
