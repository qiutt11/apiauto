#-*- encoding:utf-8 -*-
import json
import unittest
from common import runMethod,logger,analyJson,savaResponse
from common.logger import logger
from data import excelUtils
from config.readConfig import readConfig
from library import ddt
from common import checkUtils
from common.dataTearing import  treatingData
import time,re,requests


d=excelUtils.doExcel() #带上模块名，不然会报错
data1 = d.getData()

global save_response_dict,cookie
save_response_dict={}
@ddt.ddt
class TestCase(unittest.TestCase):
    @ddt.data(*data1)
    def test_case(self, A):
        """
        test report description
        :return:
        """
        # print("测试用例数据：%s"%aaaa)
        caseId = A['caseId']
        interface = A['interface']
        url=A['url']
        isRun=A['isRun']
        method=A['method']
        data=A['data']
        data_depend = A['data_depend']
        data_key = A['data_key']
        headers = A['headers']
        header_depend = A['header_depend']
        header_key = A['header_key']
        expected=A['expected']
        check_type = A['check_type']
        aduit=A['aduit']
        workflowid=A['workflowid']
        #sql = A['sql']
        # exceptlist=list(expected.split(','))
        #url=self.config.get_http("service")+url
        if isRun.lower()=='yes':
            self.logger.info("*********************************执行{}开始***********************".format(interface))
            global save_response_dict
            if re.findall("(http.+?)",url):
                url=url
            else:
                url=self.teardata.treating_url(url,save_response_dict)
                url = self.baseUrl + url
            print("请求url地址：{}；请求方式:{}".format(url,method))
            self.logger.info("请求url地址：{};请求方式{}".format(url,method))
            #requestData=analyData.analyData(data).getEncryData()
            # print("save_response_dict实际数据：%s" % save_response_dict)
            # print("data_depend %s" % data_depend)
            # print("data_key %s" % data_key)
            #print("save_response_dict测试书 %s" % save_response_dict)
            if aduit == "yes":
                self.teardata.treating_aduit(workflowid, save_response_dict)

            requestData=self.teardata.treating_data(data_depend,data_key,data,save_response_dict)
            # requestData = json.loads(data)
            # requestData = json.dumps(requestData)
            print('最终入参：%s'%requestData)
            self.logger.info('最终入参：{}'.format(requestData))
            # print("header_depend %s" % header_depend)
            # print("header_key %s" % header_key)
            # print("headers %s" % headers)
            requestHeaders=self.teardata.treating_header(header_depend,header_key,headers,save_response_dict)
            print('headers最终入参：%s' % requestHeaders)
            #requestHeaders =json.loads(requestHeaders)
            #print('headers最终入参：%s' % requestHeaders)
            #self.logger.info('headers：{}'.format(headers))

            res = self.runMethod.runRequest(method, url, requestData, requestHeaders)

            #print("反参：%s"%res.json())
            print("反参：%s" % res.text)
            #self.logger.info('{}反参：{}'.format(interface, res.json()))
            #self.logger.info('{}反参：{}'.format(interface, res.json()))
            assertRs = checkUtils.CheckUtils(res)
            actually = assertRs.run_check(check_type, expected)
            #print("actually%s" % actually["check_result"])
            # 保存token到列表
            ss=actually["check_result"]
            # if aduit=="yes":
            #     self.teardata.treating_aduit(workflowid,save_response_dict)

            #print("ss%s" % ss)
            #print("ac%s" % actually["check_result"])
            self.assertTrue(ss)
            if ss==True and  check_type!='none'  :
               save_response_dict = self.saveresponse.save_actual_response(caseId, res.json(),save_response_dict)

            #print("save_response_dict数据依赖字典数据%s" % save_response_dict)
            # if actually["check_result"] == True:
            #     token = self.analyJson.getkey_value(res.json(), "token")
            #     global dependentres
            #     dependentres = saveresponse.save_actual_response(caseId, token)
            #     print("数据依赖字典数据%s" % dependentres)
                #return True
            # else:
            #     return False

    @classmethod
    def setUp(self):
        """
        :return:
        """
        print("******************测试开始前准备*******************")
        self.runMethod = runMethod.runMethod()
        self.logger = logger
        self.config = readConfig()
        self.analyJson=analyJson.analyJson()
        self.baseUrl=self.config.get_http("service")
        self.saveresponse=savaResponse.saveResponse()
        self.teardata=treatingData()


    @classmethod
    def tearDown(self):
        print("******************{interface}测试结束，输出log完结********************")
        self.logger.info('*********************************测试结束，输出log结束*******************************')
