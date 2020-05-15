# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 用于构建邮件头
from email.header import Header
# 在邮件发送中创建一个带附件的实例
from email.mime.multipart import MIMEMultipart

# 发信服务器
smtp_server = 'smtp.qq.com'


# 发信方的信息：发信邮箱，QQ邮箱授权码  # 不需要你QQ邮箱的密码,需要授权码就行
from_addr = '919762350@qq.com'
password = 'jjtrwaudfrgebbgj'

# 收信方邮箱
to_addr = '919762350@qq.com'

# 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
# msg = MIMEText('国贸大厦今日统计的进出人数以及温度情况。详细内容见附件','plain','utf-8')

msg = MIMEMultipart()
msg.attach(MIMEText('国贸大厦今日统计的进出人数以及温度情况。详细内容见附件','plain','utf-8')) #放入邮箱的正文

# 创建邮箱的附件

# 读取本地的文件内容;构造附件
att = MIMEText(open('../excel/楼宇安防_日报.xls','rb').read(), 'based64','utf-8')
att['Content-Type'] = 'application/octet-stream'
att['Content-Disposition'] = 'attachment; filename = "day_report.xls"'


# 在把附件附上去
msg.attach(att)


# 邮件头信息
msg['From'] = Header(from_addr)
msg['To'] = Header(to_addr)
msg['Subject'] = Header('日报')



# 开启发信服务，这里使用的是加密传输
server = smtplib.SMTP_SSL(host='smtp.qq.com')
# 连接服务器 ,这里是QQ邮箱的端口
server.connect(host='smtp.qq.com', port=465)
# 登录发信邮箱
server.login(from_addr, password)
# 发送邮件
server.sendmail(from_addr, to_addr, msg.as_string())
# 关闭服务器
server.quit()
