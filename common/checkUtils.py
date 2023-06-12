# -*- coding: utf-8 -*-
#@File ：check_utils.py
#@Auth ： wwd
#@Time ： 2020/12/10 7:18 下午
import requests
import json,jsonpath
import re
from common.logger import  logger

class CheckUtils(object):
    def __init__(self,response_data):
        self.response_data = response_data
        self.check_rules = {  #判断规则和方法名去对应的一个过程
            'none': self.none_check,
            'json_key': self.body_key_check,   #'json_key': self.key_check,
            'json_key_value': self.body_key_value_check,    #'json_key_value':self.key_value_check,
            'body_regexp': self.regexp_check,
            'header_key': self.header_key_check,#比对响应头
            'header_key_value': self.header_key_value_check, #比对响应头和它对应的值
            'response_code': self.response_code_check,
            'jsonpath_value': self.jsonpath_value

        }
        self.pass_result = {
            'code':0, # 状态吗，0表示断言成功
            'response_code':self.response_data.status_code,
            'response_reason':self.response_data.reason,
            'response_headers':self.response_data.headers,
            'response_body':self.response_data.text,
            'response_url':self.response_data.url,
            'message': '测试用例执行通过',
            'check_result': True
        }
        self.fail_result = {
            'code':1,
            'response_code':self.response_data.status_code,
            'response_reason':self.response_data.reason,
            'response_headers':self.response_data.headers,
            'response_body':self.response_data.text,
            'response_url':self.response_data.url,
            'message': '测试用例执行失败',
            'check_result': False
        }

    def none_check(self):
        return self.pass_result

    def __key_check(self,actual_result,check_data):  #做成公共的私有的内置方法
        #print('111')
        key_list = check_data.split(',')
        tmp_result = []
        #print(key_list)
        #print(self.response_data.json().keys())
        for key in key_list:
            if key in actual_result.keys():
                tmp_result.append( self.pass_result )
            else:
                tmp_result.append( self.fail_result )
        if self.fail_result in tmp_result:
            # error_message = '实际结果：%s ；期望结果：%s 不相符，断言失败' % (self.response_data.text, check_data)
            # logger.error(error_message)
            # self.fail_result["message"] = error_message
            return self.fail_result
        else:
            # pass_message = '际结果：%s ；期望结果：%s 相符，断言通过' % (self.response_data.text, check_data)
            # logger.info(pass_message)
            # self.pass_result["message"] = pass_message
            return self.pass_result

    def header_key_check(self,check_data): #检查头部的
        return self.__key_check(self.response_data.headers,check_data)
    def body_key_check(self,check_data): #检查正文的
        return self.__key_check(self.response_data.json(),check_data)

    def __key_value_check(self,actual_result,check_data):
        key_value_dict = json.loads( check_data )
        tmp_result = []
        for key_value in key_value_dict.items():
            if key_value in actual_result.items():
                tmp_result.append( self.pass_result )
                print
            else:
                tmp_result.append( self.fail_result )
        if self.pass_result in tmp_result:
            # error_message = '实际结果：%s ；期望结果：%s 不相符，断言失败' % (self.response_data.text, check_data)
            # logger.error(error_message)
            # self.fail_result["message"] = error_message
            return self.pass_result
        else:
            # pass_message = '际结果：%s ；期望结果：%s 相符，断言通过' % (self.response_data.text, check_data)
            # logger.info(pass_message)
            # self.pass_result["message"] = pass_message
            return self.fail_result
    def header_key_value_check(self,check_data):
        return self.__key_value_check(self.response_data.headers,check_data)
    def body_key_value_check(self,check_data):
        return self.__key_value_check(self.response_data.json(),check_data) #这里需要json因为是键值对

    def response_code_check(self,check_data):
        if self.response_data.status_code == int(check_data):
            # error_message = '断言类型[response_code]-->实际结果：%s ；期望结果：%s 不相符，断言失败' % (self.response_data.text, check_data)
            # logger.error(error_message)
            # self.fail_result["message"] = error_message
            return self.pass_result
        else:
            # pass_message = '断言类型[response_code]-->实际结果：%s ；期望结果：%s 相符，断言通过' % (self.response_data.text, check_data)
            # logger.info(pass_message)
            # self.pass_result["message"] = pass_message
            return self.fail_result

    def regexp_check(self, check_data):
        tmp_result = re.findall(check_data, self.response_data.text)#这里需要字符串/txt
        if tmp_result:
            pass_message = '断言类型[body_regexp]-->实际结果：%s ；期望结果：%s 相符，断言通过' % (self.response_data.text, check_data)
            logger.info(pass_message)
            self.pass_result["message"] = pass_message
            return self.pass_result
        else:
            error_message = '断言类型[body_regexp]-->实际结果：%s ；期望结果：%s 不相符，断言失败' % (self.response_data.text, check_data)
            #logger.error(error_message)
            self.fail_result["message"] = error_message
            return self.fail_result
    def jsonpath_value(self,check_data):
        tmp_result = []
        check_data=json.loads(check_data)
        for k,v in check_data.items():
            print("result chekek_data %s " % k)
            try :
                actually=jsonpath.jsonpath(json.loads(self.response_data.text),k)[0]
            except TypeError :
                actually=False
            print("actually %s" % actually)
            print("vvvvvvv %s" % v)
            if v == 'None':
                v = None
            if v == 'False':
                v = False
            if actually==v:
                tmp_result.append(self.pass_result)
            else:
                tmp_result.append(self.fail_result)
        if    self.fail_result in tmp_result:
            return self.fail_result
        else:
            return self.pass_result
    def run_check(self,check_type,check_data):
        if check_type=="none" or check_data == '':
            return self.check_rules[check_type]()
        else:
            return self.check_rules[check_type](check_data)


if __name__=='__main__':
    s = requests.session()
    param = {
    "systemVParam": {
        "requestID": "自动化测试",
        "decisionEngineID": "ENGINE_NO376733836015177728",
        "championChallengeRandomNbr": [
            {
                "randomName": "R1",
                "randomNbr": 45
            }
        ]
    },
    "customField": {
        "Test": {
            "age": "18",
            "name": "孙文",
            "black": "0",
            "ceshi": "100",
            "fuzhai": "1000",
            "game": "10"
        },
        "INPUT_COMPANY_VARIABLE": {
            "name": "中青信用",
            "code": "1111111111111111",
            "representative": "王慧轩",
            "capital": "30000",
            "date": "2016-1-1",
            "phone": "121021212121",
            "address": "四川省成都市高新区交子金融科技中心A座219",
            "scope": "经验范围"
        }
    }
}
    headers={"Content-Type": "application/json"}
    url="http://10.10.10.229:9008/v2/engine/out"
    response = s.request('POST',url=url,data=json.dumps(param) ,headers=headers)
    print("ss:%s"% response)
    #response.encoding = response.apparent_encoding

#     #print(response.headers)
    data={'SystemParam': {'strategyCategoryVersion': '1.0', 'taskCode': 2000, 'decisionEngineVersion': '1.1', 'strategyCategoryId': 'LIST_NO389477013985824768', 'decisionEngineName': '自动化测试', 'strategyCategoryName': '测试策略分类', 'decisionEngineID': 'ENGINE_NO389476922797461504', 'decisionEngineStartTime': '2022-04-19 14:04:45.091', 'championChallengeRandomNbr': [{'randomName': 'R1', 'randomNbr': 45}], 'requestID': '自动化测试', 'caseID': 'RECORD_202204191404450567b48d890e1000', 'decisionEngineStopTime': '2022-04-19 14:04:45.091', 'message': 'SUCESS!'}, 'DerivedVariable': [{'VarSourceComponentName': 'shu', 'VarLable': 'null', 'VarValue': '通过', 'VarSourceComponentType': '决策树', 'VarSourceComponentLable': '决策树', 'VarType': 'null', 'VarSourceComponentID': 'LIST_NO389476943068532736'}, {'VarSourceComponentName': 'pingfenka', 'a': '10.00', 'VarLable': '', 'VarValue': '10.00', 'VarSourceComponentType': '评分卡', 'VarSourceComponentLable': '评分卡', 'VarType': '', 'VarSourceComponentID': 'LIST_NO389476967647154176'}, {'VarSourceComponentName': 'pingfenka', 'a': '0.00', 'VarLable': '', 'VarValue': '0.00', 'VarSourceComponentType': '评分卡', 'VarSourceComponentLable': '评分卡', 'VarType': '', 'VarSourceComponentID': 'LIST_NO389476967647154176'}, {'VarSourceComponentName': 'pingfenka', 'a': '90.00', 'VarLable': '', 'VarValue': '90.00', 'VarSourceComponentType': '评分卡', 'VarSourceComponentLable': '评分卡', 'VarType': '', 'VarSourceComponentID': 'LIST_NO389476967647154176'}], 'DecisionflowInfo': {'DecisionFlowResult': '001', 'DecisionflowName': '决策流', 'DecisionFlowDetailList': [{'DecisionComponentVersion': '1.0', 'DecisionComponentTypeSequence': 1, 'DecisionComponentLable': 'juecebiao', 'DecisionComponentName': '决策表', 'DecisionComponentMappingDetail': [{'componentMappingLabel': 'null', 'componentMappingName': 'null'}], 'DecisionComponentType': '决策表', 'DecisionComponentBasis': {'fuzhai': '1000', 'age': '18'}, 'DecisionComponentID': -1, 'DecisionComponentResult': '100'}, {'DecisionComponentVersion': '1.0', 'DecisionComponentTypeSequence': 2, 'DecisionComponentLable': 'shu', 'DecisionComponentName': '决策树', 'DecisionComponentMappingDetail': [{'componentMappingLabel': 'null', 'componentMappingName': 'null'}], 'DecisionComponentType': '决策树', 'DecisionComponentBasis': {'black': '0', 'age': '18'}, 'DecisionComponentID': -1, 'DecisionComponentResult': '通过'}, {'DecisionComponentVersion': '1.0', 'DecisionComponentTypeSequence': 3, 'DecisionComponentLable': 'guizeji', 'DecisionComponentName': '规则集', 'DecisionComponentType': '规则集', 'DecisionComponentBasis': '(年龄|age(age:18,age:18,))', 'DecisionComponentResultName': '拒绝', 'DecisionComponentID': -1, 'DecisionComponentResult': '001', 'DecisionComponentDetail': [{'RuleLable': 'isage', 'RuleCode': 'age', 'RuleName': '年龄'}]}, {'DecisionComponentVersion': '1.0', 'DecisionComponentTypeSequence': 4, 'DecisionComponentLable': 'pingfenka', 'DecisionComponentName': '评分卡', 'DecisionComponentMappingDetail': [{'componentMappingLabel': 'null', 'componentMappingName': 'null'}], 'DecisionComponentType': '评分卡', 'DecisionComponentBasis': {'black': '0,得分10.00', 'age': '18,得分0.00,得分90.00'}, 'DecisionComponentID': -1, 'DecisionComponentResult': '100.0', 'DecisionComponentDetail': {'ScorecardBValue': '', 'ScorecardScoreDetail': [{'ScorecardCharacterVarName': 'black', 'ScorecardBinLabel': '11', 'ScorecardCharacterVarWeight': '10', 'ScorecardPartialScore': '100.0'}, {'ScorecardCharacterVarName': 'age', 'ScorecardBinLabel': 'cehi', 'ScorecardCharacterVarWeight': '90', 'ScorecardPartialScore': '0.0'}, {'ScorecardCharacterVarName': 'age', 'ScorecardBinLabel': 'cehi', 'ScorecardCharacterVarWeight': '90', 'ScorecardPartialScore': '100.0'}], 'ScorecardInitialScore': '100.0', 'ScorecardKS': '', 'ScorecardODDS': '', 'ScorecardBaseScore': '', 'ScorecardAValue': '', 'ScorecardFinalScore': '100.0', 'ScorecardPDO': ''}}, {'DecisionComponentVersion': '1.0', 'DecisionComponentTypeSequence': 5, 'DecisionComponentLable': 'juecejisuan', 'DecisionComponentName': '决策计算', 'DecisionComponentType': '决策计算', 'DecisionComponentBasis': {}, 'DecisioncalculationResult': '100', 'DecisionComponentID': -1, 'DecisionComponentResult': ' "100"'}], 'DecisionflowId': 'LIST_NO389476982440464384', 'LastStepName': '决策计算'}, 'DecisioncalculationResult': '"100"'}
#     # print( checkUtils.key_check('access_token,expires_in') )
#     # print( checkUtils.key_value_check('{"expires_in":7200}') )
#     print( checkUtils.run_check('json_key','data') )
#     #print( checkUtils.run_check('json_key_value','{"expires_in":7200}') )
    checkUtils =CheckUtils(response)
    print(checkUtils.run_check('json_key_value', '{"strategyCategoryName": "测试策略分类"}'))
#     #print(checkUtils.run_check('header_key', 'Connection,Content-Length'))
#    # print( checkUtils.run_check('header_key_value','{"Connection":"keep-alive"}') )#键值对
    aa=re.findall('"strategyCategoryName": "测试策略分类"',json.dumps(data))
    print("aaaaaaaaaaa %s" % aa)
