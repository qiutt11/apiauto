#-*- encoding:utf-8 -*-
"""
自己创建的一个读取配置文件的类
"""
import os
import configparser
from common.contains  import *


#第二种方法
class ReadConfig(configparser.ConfigParser):

    def __init__(self,dir):
        # 实例化对象
        super().__init__()
        # 加载文件

        self.read(dir, encoding='utf-8')






