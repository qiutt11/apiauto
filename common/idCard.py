# -*- coding: utf-8 -*-
import random
from datetime import date, datetime
import string
import os
import datetime

def get_idcard(maxage=60, minage=20):
    '''随机生成身份证号码'''
    now = date.today()
    birth = now.year - int(minage)
    mon = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10', '11', '12']
    mon_days = ['31', '28', '31', '30', '31', '30', '31', '31','30', '31', '30', '31']
    age = int(maxage) - int(minage)
    y = str(birth - random.randint(1, age))
    index1 = random.randint(0, 11)
    m = str(mon[index1])
    m = m.zfill(2)
    maxDay = int(mon_days[index1])
    d = str(random.randint(1, maxDay))
    d = d.zfill(2)
    s = y + m + d
    area = ["11", "12", "13", "14", "15", "21", "22", "23", "31", "32", "33", "34", "35", "36", "37", "41", "42", "43", "44","45", "46", "50", "51", "52", "53", "54", "61", "62", "63", "64", "65", "71", "81", "82", "91"]
    # area = ["15"] #选择哪个区域这个传哪个区域码
    id = random.choice(area)+''.join(random.choice(string.digits) for i in range(4))+s+''.join(random.choice(string.digits) for i in range(3))
    id = id[0:17]
    lid = list(id)
    temp = 0
    for nn in range(2, 19):
        a = int(lid[18 - nn])     # 17到1的数
        w = (2 ** (nn - 1)) % 11  # 17到1的系数
        temp += a * w             # temp = temp+a*w 17位数字和系数相乘的结果相加
    temp = (12 - temp % 11) % 11
    if temp >= 0 and temp <= 9:
        id += str(temp)
    elif temp == 10:
        id += 'X'
    return id

if __name__ == '__main__':

    aa=get_idcard()
    print(aa)