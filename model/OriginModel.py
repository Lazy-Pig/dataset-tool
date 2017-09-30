# coding: utf-8
import logging


class OriginModel(object):
    """
    实现了Analyzing Android Encrypted Network Traffic to Identify User Actions的算法
    """
    def __init__(self, train_dataset):
        self.train_dataset = train_dataset

    def learn(self):
        logging.info("learn方法还没有实现哦")
        pass