#-*- encoding:utf-8 -*-

# author:授客

import re

def parse_sub_expr(sub_expr):

    '''

    解析字表达式-元素路径的组成部分

    :paramsub_expr:

    :return:

    '''

    RIGHT_INDEX_DEFAULT = '200000000' # 右侧索引的默认值 未指定右侧索引时使用，形如 key[2:]、key[:]

    result = re.findall('.+ ', sub_expr)

    if result: # 如果子表达式为数组，形如 [1]、key[1]、 key[1:2]、 key[2:]、 key[:3]、key[:]

        array_part = result[0]

        array_part = array_part.lstrip('[').rstrip(']')

        key_part = sub_expr[:sub_expr.index('[')]

        if key_part == '$':# 如果key为 $ ，为根，替换为数据变量 json_data

            key_part = JSON_DATA_VARNAME

        elif key_part == '*':

            key_part == '.+' # 如果key为 * ，替换为\.+ 以便匹配 ["key1"]、["key2"]、……

        else:

            key_part = ' " ' % key_part

        if array_part == '*': # 如果数组索引为 * ，替换为\d+ 以便匹配 [0]、[1]、……

            array_part = ' \d+'

        else:

            array_part_list = array_part.replace(' ', '').split(':')

            left_index = array_part_list[0:1]

            right_index = array_part_list[1:]

            if left_index:

                left_index = left_index[0]

                if not (left_index or left_index.isdigit()): # 为空字符串、非数字

                    left_index = '0'

            else:

                left_index = '0'

            if right_index:

                right_index = right_index[0]

                if not (right_index or right_index.isdigit()):

                    right_index = RIGHT_INDEX_DEFAULT # 一个比较大的值，

                    array_part = left_index + '-' + right_index

            else:

                    array_part = left_index

                    array_part = ' [' % array_part# 数组索引设置为    [n−m]    ,以便匹配[n],[n+1], ……，[m-1]

        return key_part + array_part

    elif sub_expr == '*':

        sub_expr = ' .+ '

    elif sub_expr == '$':

        sub_expr = JSON_DATA_VARNAME

    else:

        sub_expr = '  " ' % sub_expr

    return sub_expr

    def parse_json(json_data, data_struct_link):

        '''

        递归解析json数据结构，存储元素的路径

        :paramjson_data:

        :paramdata_struct_link:

        :return:

        '''

        if type(json_data) == type({}): # 字典类型

            keys_list = json_data.keys()

            for key in keys_list:

                temp_data_struct_link =  data_struct_link + '["%s"]' % key

                if type(json_data[key]) not in [type({}), type([])]: # key对应的value值既不是数组，也不是字典

                    data_struct_list.append(temp_data_struct_link)

                else:

                    parse_json(json_data[key], temp_data_struct_link)

        elif type(json_data) == type([]): # 数组类型

            array_length = len(json_data)

            for index in range(0, array_length):

                temp_json_data = json_data[index]

                keys_list = temp_json_data.keys()

                for key in keys_list:

                    temp_data_struct_link =  data_struct_link + '[%s]["%s"]' % (str(index), key)

                    if type(temp_json_data[key]) not in [type({}), type([])]: # key对应的value值既不是数组，也不是字典

                        data_struct_list.append(temp_data_struct_link)

                    else:

                        parse_json(temp_json_data[key], temp_data_struct_link)

if __name__ == '__main__':

    pass