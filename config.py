# coding: utf-8

"""
全局配置
"""
# 手机的ip
host_ip = '10.42.0.166'

# 存储数据集的目录
dataset_path = "dataset"

# 过滤后的跟目标app相关的ip存储路径
save_ips_path = 'weibo_out/save_ips.pkl'


"""
抓包相关的配置
"""
# 要抓包的网卡名称
device = "wlp2s0"

# BPF过滤规则
filter_rule = "host 10.42.0.166"


"""
训练相关的配置
"""
# 数据集
from preprocessor.AllLengthData import AllLengthData
dataset_preprocessor = AllLengthData

# 训练模型
from model.DynamicLSTM import DynamicLSTM
train_model = DynamicLSTM