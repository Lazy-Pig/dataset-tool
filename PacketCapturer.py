# coding: utf-8

import pcapy
import threading
import config
import logging
from PyQt4 import QtCore

logger = logging.getLogger("log")

class PacketCapturer(threading.Thread):
    def __init__(self):
        super(PacketCapturer, self).__init__()
        self.device = config.device
        self.is_capture_enable = False

    def _handle_packet(self, header, data):
        if self.is_capture_enable:
            logger.debug(QtCore.QString(u"抓到包了"))
            # TODO:把抓到的包存下来
        else:
            logger.debug(QtCore.QString(u"抛弃这个包"))

    def enable_capture(self):
        self.is_capture_enable = True

    def disable_capture(self):
        self.is_capture_enable = False

    def run(self):
        pcap = pcapy.open_live(self.device, 1500, 0, 100)
        # pcap.setfilter("")
        pcap.loop(0, self._handle_packet)
