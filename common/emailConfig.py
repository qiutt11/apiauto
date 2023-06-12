import unittest
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
from config.readConfig import readConfig
class emailConfig():
    def send_mail(self,file_new):
        #-----------1.跟发件相关的参数------
        config1=readConfig()
        smtpserver ='smtphz.qiye.163.com'              #发件服务器
        port = 994                     #端口
        username = '自动化测试'  #发件箱用户名
        password =  config1.get_email("password")
        sender = config1.get_email("address")
        #receiver = ['qiutiantian@cycredit.com.cn','liling@cycredit.com.cn'] #收件人邮箱
        #receiver = config1.get_email("cc")
        receiver=['tiantian.qiu@hcr.com.cn'] #收件人邮箱
        # ----------2.编辑邮件的内容------
        #读文件
        f = open(file_new, 'rb')
        mail_body = f.read()
        f.close()
        #mail_body="接口自动化结果，请查看附件内容"
        # 邮件正文是MIMEText
        body = MIMEText("接口自动化结果，请查看附件内容", 'html', 'utf-8')
        # 邮件对象
        msg = MIMEMultipart()
        msg['Subject'] = Header("自动化测试报告", 'utf-8').encode()#主题
        #msg['From'] = Header(u'测试机 <%s>'%sender)
        #msg['From'] = Header(u'测试机 <%s>')  #发件人
        msg['To'] = Header(u'测试负责人 <%s>'%receiver)            #收件人
        msg['To'] = ';'.join(receiver)
        #print("msg['To'] %s" % msg['To'])
        msg['date'] = time.strftime("%a,%d %b %Y %H:%M:%S %z")
        msg.attach(body)
        # 附件
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename="test_report.html"'
        msg.attach(att)
        # ----------3.发送邮件------
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver)  # 连服务器
            smtp.login(sender, password)
        except:
            smtp = smtplib.SMTP_SSL(smtpserver, port)
            smtp.login(sender, password)  # 登录

        smtp.sendmail(sender, receiver, msg.as_string())  # 发送
        smtp.quit()
        # #发送邮件
        # smtp = smtplib.SMTP()
        # smtp.connect(‘smtp.mxhichina.com‘)  # 邮箱服务器
        # smtp.login(username, password)  # 登录邮箱
        # smtp.sendmail(sender, receiver, msg.as_string())  # 发送者和接收者
        # smtp.quit()
        print("邮件已发出！注意查收。")

    def new_report(self,test_report):
        lists = os.listdir(test_report)  # 列出目录的下所有文件和文件夹保存到lists
        lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))  # 按时间排序
        file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
        print(file_new)
        return file_new