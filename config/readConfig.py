#-*- encoding:utf-8 -*-
import os
import configparser


# path=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# configPath=os.path.join(path,'config\\125config.ini')
# config=configparser.ConfigParser()
# config.read(configPath,encoding='utf-8')
class readConfig():
    def __init__(self):
        self.path=os.path.abspath(os.path.dirname(__file__))
        self.configPath=os.path.join(self.path,'conf.ini')
        #self.configPath=os.path.join(self.path,'config\\')
        #self.configpath=os.path.join(self.configPath,configname)
        self.config=configparser.ConfigParser()
        self.config.read(self.configPath,encoding='utf-8')

    def get_http(self,name):
        value=self.config.get('HTTP',name)
        return value
    def get_user(self,name):
        value=self.config.get('USER',name)
        return value
    def get_email(self,name):
        value=self.config.get('EMAIL',name)
        return value
# if __name__=='__main__':
#     a=readConfig()
#     b=a.get_http("service")
#     print(b)
