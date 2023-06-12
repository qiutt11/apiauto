import unittest
import os,re,json
import time

from common.emailConfig import emailConfig
#import HTMLTestRunner
from library.HTMLTestRunnerNew import HTMLTestRunner

# libs = {"flask","ddt","pymysql","requests","openpyxl",'retrying','xlrd','PyCryptodome','paramunittest','jsonPath','jsonpath_rw','jsonpath_ng','xpinyin'} # 将需要安装的库名称放到列表中
# for lib in libs:
#         os.system("pip3 install  "+lib+" -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com")

# 用例路径
case_path = os.path.join(os.getcwd(), 'case')
# 报告存放路径
report_path = os.path.join(os.getcwd(), 'report')

def all_case():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="testCase.py", top_level_dir=None)
    print(discover)
    return discover


if __name__ == '__main__':
    # 获取当前时间，这样便于下面的使用
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # html报告文件路径
    report_abspath = os.path.join(report_path, 'report' + now + '.html')
    # 打开一个文件，将result写入此file中
    fp = open(report_abspath, 'wb')
    runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告，测试结果如下：',
                                           description='用例执行情况：')
    # 调用all_case函数返回值
    runner.run(all_case())
    fp.close()
    path=os.path.abspath(os.path.dirname(__file__))
    test_path = os.path.join(path,'report')
    new_report=emailConfig().new_report(test_path)
    emailConfig().send_mail(new_report)


