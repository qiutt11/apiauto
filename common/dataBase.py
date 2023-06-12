
import pymysql
def dataBase():


     db=pymysql.connect(
         host='192.168.15.213',
         port=15306,
         user='oms_user',
         passwd='oms#123f',
         db='oms_hr',
        charset='utf8'
     )
     return db