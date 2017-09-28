# coding: utf-8

"""
全局配置
"""
# 手机的ip
host_ip = '10.42.0.166'


"""
抓包相关的配置
"""
# 要抓包的网卡名称
device = "wlp2s0"

# BPF过滤规则
filter_rule = "host 10.42.0.166"


"""
抓包相关的配置
"""
# 存储数据集的目录
dataset_path = "dataset"

# 过滤后的跟目标app相关的ip存储路径
save_ips_path = 'weibo_out/save_ips.pkl'

# 数据集
from preprocessor.AllLengthData import AllLengthData
dataset_preprocessor = AllLengthData