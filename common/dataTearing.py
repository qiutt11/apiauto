
import json,re
import jsonpath
from  common.logger import logger
from json import JSONDecodeError
from common.savaResponse import saveResponse
from common.analyJson import analyJson
from  common.aduit import aduit
from common.idCard import get_idcard
from common.randomName import RandomName
from xpinyin import Pinyin
from common.randomPhone import randomPhone


class treatingData(object):
    def __init__(self):
        self.analyJson=analyJson()
        pass
    def treating_header(self,header_depend,header_key,headers,save_response_dict):
        #使用哪个header
        if header_depend=='' or header_depend==None:
            headers=json.loads(headers)
            logger.info(f'headers没有依赖数据{headers}')
        else:
            if header_key=="" or header_key==None:
                headers=json.loads(headers)
                logger.error(f'headers有依赖数据，依赖数据key未获取到{headers}')
            else:
                headers_dict=json.loads(header_key)
                ss = saveResponse()
                #print("header_depend %s" % header_depend)
                #print("save_response_dict121212 %s" % save_response_dict)
                dependent_dict =ss.read_depend_data(header_depend,save_response_dict)
                #print("dependent_dict %s" %dependent_dict)
                headers = json.loads(headers)
                for k,v in headers_dict.items():
                    depend_v=self.analyJson.getkey_value(dependent_dict,v)
                    # print("depend_v %s" % depend_v)
                    # print("k11111 %s" % k)
                    #print("headers %s" % type(headers))
                    headers=self.analyJson.repkey_value(headers,k,depend_v)
                    #print("depend_v_headers::::: %s" % headers)
        return headers

    #处理依赖数据data
    def treating_data(self, data_depend, data_key, data,save_response_dict):
            if data_depend=='' or data_depend==None:

                  data =data
                  logger.info(f'data没有依赖数据{data}')
            else:
                if data_key=='' or data_key==None:

                    data = data
                    logger.error(f'data有依赖数据，依赖数据key未获取到{data}')
                else:
                    ss=saveResponse()
                    data = json.loads(data)
                    #print("dataloads后数据 %s" % data)
                    dependent_data = ss.read_depend_data(data_depend,save_response_dict)
                    logger.debug(f'依赖数据解析获得的字典{dependent_data}')
                    # 合并组成一个新的data
                    data_dict = json.loads(data_key)
                    #print("data_dict数据 %s" % data_dict)
                    logger.info(f"data_dict:{data_dict}")
                    for k,v in data_dict.items():
                        print("k数据 %s" % k)
                        isjavacode=re.findall("(JAVACODE.+?)",k)
                        print("isjavacode %s"  % isjavacode)
                        if isjavacode!=[]:
                            print("kjava %s"% k)
                            print("kvvvv %s"% v)
                            print("javacode中得data ：%s"% data)
                            data=json.dumps(data)
                            print("dependent_data：：：：： %s" % dependent_data)
                            value=self.analyJson.getkey_value(dependent_data, v)
                            print("kvalue %s" % value)
                            data=data.replace(k,value)
                            print("javadata %s" %data)
                            data=json.loads(data)
                        else:
                            depend_v = self.analyJson.getkey_value(dependent_data, v)
                            #print("depend-v ::::%s" % depend_v)
                            logger.info(f"depend_v:{depend_v}")
                            #print("其他data %s" % data)
                            data = self.analyJson.repkey_value(data, k, depend_v)
                            #print("其他改变后data %s" % data)
                            logger.info(f"{k}数据下:{data}")
                    for k,v  in  data.items():
                         if k=="idCard":
                             global idCard
                             idCard=get_idcard()
                             data=self.analyJson.repkey_value(data,"idCard",idCard)
                         elif k=="realName":
                             random_name_obj = RandomName()
                             global realName
                             realName=random_name_obj.get_name()
                             data = self.analyJson.repkey_value(data, "realName", realName)

                         if v=="shi.ce1@hcr.com.cn":
                             global email
                             p=Pinyin()
                             email=p.get_pinyin(realName)+'@hcr.com.cn'
                             print(email)
                             data=self.analyJson.repkey_value(data,k,email)
                         if v=='13077622987':
                             global phone
                             phone=randomPhone()
                             data=self.analyJson.repkey_value(data,k,phone)

                    data = json.dumps(data)
                    logger.info(f'data有数据，依赖有数据时{data}')
            return data
    def treating_url(self,url,save_response_dict):
        # #处理路径参数path
        # # 传进来的参数类似 {"case_002":"$.data.id"}/item/{"case_002":"$.meta.status"}，进行列表拆分
        path_list=url.split('/')
        #
        for i in range(len(path_list)):
            parameters_pa_url=''
            if re.findall("=", path_list[i]):
                url_list=path_list[i].split("=")
                try:
                    url_dict = json.loads(url_list[-1])
                except JSONDecodeError as e:
                    logger.info(f'无法转换字典，进入下一个检查，本轮值不发生变化：{url_list[-1]},{e}')
                    continue
                else:
                    logger.info(f'url_l,{url_list[-1]}')
                    # 处理json.loads('数字')正常序列化导致的AttributeError
                    try:
                        # 尝试从对应的case实际响应提取某个字段内容
                        for k, v in url_dict.items():
                            try:
                                # 尝试从对应的case实际响应提取某个字段内容
                                logger.info(f"k:{k}")
                                logger.info(f"v:{v}")
                                url_list[-1] = jsonpath.jsonpath(save_response_dict[k], v)[0]
                            except TypeError as e:
                                logger.error(f'无法提取，请检查响应字典中是否支持该表达式，{e}')
                    except AttributeError as e:
                        logger.error(f"类型错误：{type(url_list[-1])}，本次将不转换值{url_list[-1]},{e}")
                url_list= map(str, url_list)
                path_list[i]="=".join(url_list)
            else:

                try:
                  path_dict=json.loads((path_list[i]))
                except JSONDecodeError as e:
                    logger.info(f'无法转换字典，进入下一个检查，本轮值不发生变化：{path_list[i]},{e}')
                    continue
                else:
                    logger.info(f'path_dict值,{path_dict}')
                    # 处理json.loads('数字')正常序列化导致的AttributeError
                    try:
                        # 尝试从对应的case实际响应提取某个字段内容
                        for k,v in path_dict.items():
                            try:
                                # 尝试从对应的case实际响应提取某个字段内容
                                logger.info(f"k:{k}")
                                logger.info(f"v:{v}")
                                path_list[i]=jsonpath.jsonpath(save_response_dict[k],v)[0]
                            except TypeError as e:
                                logger.error(f'无法提取，请检查响应字典中是否支持该表达式，{e}')
                    except AttributeError as e:
                        logger.error(f"类型错误：{type(path_list[i])}，本次将不转换值{path_list[i]},{e}")
        # 字典中存在有不是str的元素:使用map 转换成全字符串的列表
        path_list=map(str,path_list)
        # 将字符串列表转换成字符：500/item/200
        parameters_path_url="/".join(path_list)
        parameters_path_url=parameters_path_url+parameters_pa_url
        logger.info(f'path路径参数解析依赖后的路径为{parameters_path_url}')
        return parameters_path_url
        #,parameters_path_url

    def treating_aduit(self,workflowid,save_response_dict):
        ss = saveResponse()
        dependent_dict = ss.read_depend_data(workflowid, save_response_dict)
        if re.findall("workflowId'",workflowid):
            workflow=self.analyJson.getkey_value(dependent_dict,'workflowId')

        else:

            workflow = self.analyJson.getkey_value(dependent_dict, 'link')
        # for k,v in workflowid.items():
        #     workflow=jsonpath.jsonpath(save_response_dict[k],v)[0]
        #
        #     logger.info(f'workflow{workflow}')

        aduit(workflow)
        return workflow

# if __name__ == '__main__':
#     response={'code': 2000, 'message': 'SUCESS!', 'date': '1646875006572', 'data': {'token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxIiwiY3JlYXRlZCI6MTY0Njg3NTAwNjU3MCwiZXhwIjoxNjQ2OTYxNDA2fQ.kBY0eCD8gyKFHaVNcskzAgFJZdjx0YroCGuUL8FfPiBouqEq6iDu9EpVxRy8xFIAEmvXdXFkZ5Ix-fJW3QGHzA', 'status': 0}, 'success': True}
#     caseid="case_001"
#     ss=saveResponse()
#     a=ss.save_actual_response(caseid,json.dumps(response))
#     #print("ss %s"% a)
#     depend= {"case_001":"['$..token', '$.date']"}
#     dependent_headers =ss.read_depend_data(json.dumps(depend))
#     headers={"Content-Type": "application/json","x-token": "","engineNo":"ENGINE_NO283669431413772288"}
#     header_key={"x-token":"token","engineNo":"date"}
#     data=treatingData()
#     aa=data.treating_header(json.dumps(depend),json.dumps(header_key),headers,ss)
#     print("aa: %s" %aa)



