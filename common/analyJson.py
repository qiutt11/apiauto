# -!- coding:utf-8 -!-
from common.logger import logger
import json
import re
#import jsonpath,parse
from jsonpath_ng import jsonpath,parse


logger=logger

# def analyze_json(jsons):
#     key_value=''
#     if isinstance(jsons,dict):
#         for key in jsons.keys():
#             key_value=jsons.get(key)
#             if isinstance(key_value,dict):
#                 analyze_json(key_value)
#             elif isinstance(key_value,list):
#                 for json_array in key_value:
#                     analyze_json(json_array)
#             else:
#                 print(str(key) + " = " + str(key_value))
#     elif isinstance(jsons,list):
#         for json_array in jsons:
#             analyze_json(json_array)
class analyJson():

    def repkey_value(self,jsons,key,value,default=None):

        if re.findall("(.+groupList.+?)",key):
            jsonpath_expr=parse(key)
            jsonpath_expr.find(jsons)
            jsonpath_expr.update(jsons,value)
            return jsons
        else:
            if isinstance(jsons,dict):
                for k in jsons.keys():
                    if k in jsons.keys():
                        if k==key:
                            jsons[key]=value
                            return jsons
                        elif  isinstance(jsons[k],dict):
                            ret=self.repkey_value(jsons[k],key,value)
                            if ret is not default:
                                return jsons
                        elif isinstance(jsons[k],list):
                            for i in jsons[k]:
                                ret=self.repkey_value(i,key,value)
                            if ret is not default:
                                return jsons

    def getkey_value(self,jsons,key,default=None):
        key_value=''
        if isinstance(jsons,dict):
            for json_result in jsons.values():
                if key in jsons.keys():
                    key_value=jsons.get(key)
                    return key_value
                else:
                    ret=self.getkey_value(json_result,key)
                    if ret is not default:
                        return ret
        elif isinstance(jsons,list):
            for json_array in jsons:
                 ret=self.getkey_value(json_array,key)
                 if ret is not default:
                     return ret


    def is_dict(self,content):
        try :
            eval(content)
        except SyntaxError:
            return False
        return True

# def getkey_value(jsononly,key,default=None):
#     if isinstance(jsononly,dict):
#         for k,v in jsononly.items():
#             if k==key:
#                 return v
#             elif isinstance(v,dict):
#                 ret=getkey_value(v,key,default=None)
#                 if ret is not default:
#                     return ret

if __name__=="__main__":
    jsons={'detailJson': '{"cells":[{"shape":"flow-edge","zIndex":0,"id":"49e2deb5-904e-4412-b08a-ddce858b8c0b","source":{"cell":"start","port":"start-port"},"target":{"cell":"c895aa2d-311c-4634-ae34-56a4c9fae216","port":"153c1470-66f5-4d9a-910e-81d744bcffa0"}},{"shape":"flow-edge","zIndex":0,"id":"7d153558-5bb8-49bf-af9c-897f3b4b6797","source":{"cell":"c895aa2d-311c-4634-ae34-56a4c9fae216","port":"21ad44b3-6741-433d-ab2b-0e6ecd82ba60"},"target":{"cell":"54ab700f-c803-40f3-97e1-bf2beec39d18","port":"f2206567-470c-48e1-802c-ba5ef007e379"}},{"position":{"x":500,"y":90},"size":{"width":70,"height":100},"attrs":{"groupTitle":{"text":"开始"},"image":{"xlink:href":"/img/icon_start.png"}},"shape":"flow-image","ports":{"groups":{"left":{"position":"left","attrs":{"circle":{"r":5,"refY":0,"refX":-1,"magnet":true,"stroke":"#5F95FF","strokeWidth":1,"fill":"transparent","style":{"visibility":"hidden"}}}},"right":{"position":"right","attrs":{"circle":{"r":5,"refY":0,"refX":-1,"magnet":true,"stroke":"#5F95FF","strokeWidth":1,"fill":"transparent","style":{"visibility":"hidden"}}}}},"items":[{"group":"left","id":"cc944a19-ae09-4ed1-af2f-6465b8b76033"},{"group":"right","id":"start-port"}]},"id":"start","data":{"nomenu":true},"zIndex":1},{"position":{"x":780,"y":140},"size":{"width":70,"height":100},"attrs":{"stencilTitle":{"text":"结束"},"groupTitle":{"text":"结束"},"image":{"xlink:href":"/img/icon_end.png"}},"shape":"flow-image","ports":{"groups":{"left":{"position":"left","attrs":{"circle":{"r":5,"refY":10,"refX":2,"magnet":true,"stroke":"#5F95FF","strokeWidth":1,"fill":"transparent","style":{"visibility":"hidden"}}}},"right":{"position":"right","attrs":{"circle":{"r":5,"refY":10,"refX":-2,"magnet":true,"stroke":"#5F95FF","strokeWidth":1,"fill":"transparent","style":{"visibility":"hidden"}}}}},"items":[{"group":"left","id":"f2206567-470c-48e1-802c-ba5ef007e379"},{"group":"right","id":"2c3188be-c6f3-4474-ab4d-07daee056beb"}]},"id":"54ab700f-c803-40f3-97e1-bf2beec39d18","data":{"type":"end","nomenu":true},"zIndex":2},{"position":{"x":640,"y":100},"size":{"width":70,"height":100},"attrs":{"stencilTitle":{"text":"决策表"},"groupTitle":{"text":"决策表"},"image":{"xlink:href":"/img/icon_juecebiao.png"},"stencilLabel":{"text":"决策表"}},"shape":"flow-image","ports":{"groups":{"left":{"position":"left","attrs":{"circle":{"r":5,"refY":10,"refX":2,"magnet":true,"stroke":"#5F95FF","strokeWidth":1,"fill":"transparent","style":{"visibility":"hidden"}}}},"right":{"position":"right","attrs":{"circle":{"r":5,"refY":10,"refX":-2,"magnet":true,"stroke":"#5F95FF","strokeWidth":1,"fill":"transparent","style":{"visibility":"hidden"}}}}},"items":[{"group":"left","id":"153c1470-66f5-4d9a-910e-81d744bcffa0"},{"group":"right","id":"21ad44b3-6741-433d-ab2b-0e6ecd82ba60"}]},"id":"c895aa2d-311c-4634-ae34-56a4c9fae216","data":{"id":102550,"engineNo":"ENGINE_NO376733836015177728","engineNoTypeId":"LIST_NO382233968345223168","name":"决策表","type":3,"englishName":"juecebiao","serviceVersion":"1.0","mappingType":null,"mappingName":null,"resultType":"java.lang.Integer"},"zIndex":3}]}', 'engineNo': 'ENGINE_NO376733836015177728', 'type': 2, 'engineNoTypeId': 'LIST_NO382627882008973312', 'serviceVersion': '1.0', 'groupList': [{'engineListNo': 'LIST_NO382627882008973312', 'engineListNoType': '1.0', 'variableList': [{'grade': 'c895aa2d-311c-4634-ae34-56a4c9fae216', 'parentId': 'start', 'engineListType': 3, 'engineListNo': 'LIST_NO382233968345223168', 'engineListNoType': '1.0', 'formula': None, 'value': None, 'decisionResult': 0}]}]}
    #token=analyJson().getkey_value(jsons,"age","value")
    #print(analyJson().rpHeader_token(token))

    key="$.groupList[0].engineListNo"
    value="LIST_NO382627882008973312"
    token=analyJson().repkey_value(jsons,key,value)
    print(token)





