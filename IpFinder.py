# coding: utf-8
import os
import sys
import re
import zipfile
import tempfile
import logging
import shutil
import glob
import pickle
from xml.dom.minidom import parse

OUTDIR = "weibo_out"
INPUTFILE = "weibo_find_ip_list2000.saz"
# OUTDIR = "xiaomi_out"
# INPUTFILE = "weibo_find_ip_list2000.saz"


class IpFinder(object):
    """
    在fiddler生成的saz文件中筛选出想要留下的ip
    """
    def __init__(self, saz_file):
        self.saz_file = saz_file
        self.save_ips = set()
        self.drop_ips = set()
        self.load_ips()

    def extract_saz(self):
        """
        将saz文件解压
        """
        # 如果输入是saz文件则解压
        if os.path.isfile(self.saz_file):
            try:
                self.tmpdir = tempfile.mkdtemp()
                logging.info("创建临时文件夹%s", self.tmpdir)
            except:
                logging.info("创建临时文件夹失败")
                sys.exit(-1)
            try:
                z = zipfile.ZipFile(self.saz_file, "r")
                logging.info("打开saz文件 %s", self.saz_file)
            except:
                logging.info("打开saz文件失败 %s", self.saz_file)
                sys.exit(-1)
            try:
                z.extractall(self.tmpdir)
                z.close()
                logging.info("将%s文件解压到%s", self.saz_file, self.tmpdir)
            except:
                logging.info("将%s文件解压到%s失败", self.saz_file, self.tmpdir)
                sys.exit(-1)
            if os.path.isdir("%s/raw/" % (self.tmpdir)):
                self.fiddler_raw_dir = "%s/raw/" % (self.tmpdir)
            else:
                logging.info("在解压后的临时文件夹中没有找到%s/raw (需要手动删除临时文件夹)", self.tmpdir)
                sys.exit(-1)

        # 如果输入是文件夹，则默认是fiddler的raw文件夹
        elif os.path.isdir(self.saz_file):
            self.fiddler_raw_dir = self.saz_file
            self.tmpdir = None
        else:
            raise Exception("输入saz的路径既不是.saz文件也不是文件夹！")

        logging.info("fiddler的raw文件准备完毕")

    def remove_tmpdir(self):
        """
        删除解压saz文件时创建的/tmp下的临时目录
        """
        if self.tmpdir:
            try:
                shutil.rmtree(self.tmpdir)
                logging.info("删除tmpdir %s", self.tmpdir)
            except:
                logging.info("删除tmpdir %s 失败", self.tmpdir)

    def parse_saz(self):
        """
        解析saz raw中的文件
        """
        if os.path.isdir(self.fiddler_raw_dir):
            m_file_list = glob.glob("%s/%s" % (self.fiddler_raw_dir, "*_m.xml"))
            m_file_list.sort()
            logging.info("一共有 %d 条记录" % len(m_file_list))
            for index, xml_file in enumerate(m_file_list):
                dom = parse(xml_file)
                m = re.match(r"^(?P<fileid>\d+)_m\.xml",os.path.basename(xml_file))
                if m:
                    fileid = m.group("fileid")
                else:
                    logging.info("failed to get fiddler id tag")
                    sys.exit(-1)

                xmlTags = dom.getElementsByTagName('SessionFlag')
                for xmlTag in xmlTags:
                    xmlTag = xmlTag.toxml()
                    m = re.match(
                        r"\<SessionFlag N=\x22x-(?:client(?:ip\x22 V=\x22[^\x22]*?(?P<clientip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|port\x22 V=\x22(?P<sport>\d+))|hostip\x22 V=\x22[^\x22]*?(?P<hostip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))\x22",
                        xmlTag)

                    if m and m.group("hostip"):
                        host_ip = m.group("hostip")

                # 当ip是一个没有见过的ip时，打印对应的域名，并询问用户要不要存到save_ips中
                if (host_ip not in self.save_ips) and (host_ip not in self.drop_ips):
                    # 在_c.txt文件中找到host
                    req = open(self.fiddler_raw_dir + fileid + "_c.txt").read()
                    m = re.match(r"^[^\r\n\s]+\s+(?P<host_and_port>https?\:\/\/[^\/\r\n\:]+(\:(?P<dport>\d{1,5}))?)\/", req)
                    if m:
                        domain = m.group("host_and_port")
                    else:
                        domain = "Unknow"
                    logging.info("%s  %s (press y to save, n to drop, s to skip, q to quit)", domain, host_ip)
                    choice = raw_input()
                    if choice == 'y':
                        self.save_ips.add(host_ip)
                        with open(OUTDIR + "/save_ips.txt", "a") as f:
                            f.write("%s %s\n" % (domain, host_ip))
                    elif choice == 'n':
                        self.drop_ips.add(host_ip)
                        with open(OUTDIR + "/drop_ips.txt", "a") as f:
                            f.write("%s %s\n" % (domain, host_ip))
                    elif choice == 'q':
                        return
                    else:
                        pass
                else:
                    logging.info("[%s]%s" % (fileid, host_ip))

                # 每解析5条记录就存一下pickle
                if index % 5 == 0:
                    with open(OUTDIR + "/save_ips.pkl", "w") as f:
                        pickle.dump(self.save_ips, f)
                    with open(OUTDIR + "/drop_ips.pkl", "w") as f:
                        pickle.dump(self.drop_ips, f)
        else:
            logging.info("fiddler raw文件夹 %s 不存在", self.fiddler_raw_dir)
            sys.exit(-1)

    def load_ips(self):
        """
        从save_ips.txt和drop_ips.txt中加载已经分类过的ip,
        分别加到save_ips和drop_ips中
        """
        if os.path.isfile(OUTDIR + "/save_ips.pkl"):
            with open(OUTDIR + "/save_ips.pkl", "r") as f:
                self.save_ips = pickle.load(f)
        if os.path.isfile(OUTDIR + "/drop_ips.pkl"):
            with open(OUTDIR + "/drop_ips.pkl", "r") as f:
                self.drop_ips = pickle.load(f)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s',
                        datefmt='%m-%d %H:%M')
    finder = IpFinder(INPUTFILE)
    finder.extract_saz()
    finder.parse_saz()
    finder.remove_tmpdir()