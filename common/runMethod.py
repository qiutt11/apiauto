import requests
import json
from common.logger import logger
from requests.adapters import HTTPAdapter


logger=logger
s=requests.session()

s.mount('http://',HTTPAdapter(max_retries=3))#重试3次
s.mount('https://',HTTPAdapter(max_retries=3))
class runMethod():
    def sendPost(self,url,data,headers=None):
        res=None
        if headers!=None:
            res = s.request('POST', url=url, data=data.encode(), headers=headers)
        else:
            res=s.request('POST',url=url,data=data.encode())
        return res

    def sendGet(self,url,data,headers):
        res=None
        if headers!=None:
            res=s.request('GET',url=url,headers=headers)
        else:
            res=s.request('GET',url=url)
        #res=json.loads(res)
        return res

    def runRequest(self,method,url=None,data=None,headers=None):
        res=None
        if method.lower()=="get":
            res=self.sendGet(url,data,headers)
            #logger.info(str(res))
        elif method.lower()=="post":
            res=self.sendPost(url,data,headers)
            print()
            #logger.info('res={}'.format(res))
        else:
            #logger.info("method方式错误")
            print("method方式错误")
        return res