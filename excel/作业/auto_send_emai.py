# -*- coding: utf-8 -*-
# @Author: 曾辉
'''
简单的统计每日进入人数和温度，并且将详细信息通过邮件发出
'''
import xlwt
import xlrd
import numpy as np
import datetime
from xlutils.copy import copy
# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 用于构建邮件头
from email.header import Header
# 在邮件发送中创建一个带附件的实例
from email.mime.multipart import MIMEMultipart

def get_excel(source_xls,save_path):
	'''

	:param source_xls:  文档的路径
	:return:
	'''
	data = xlrd.open_workbook(source_xls)

	# 创建一个新的工作簿
	wb = xlwt.Workbook()
	# 把读取到的工作簿的内容全部复制到 新的工作簿上
	wb = copy(data)

	for i in range(len(data.sheets())):
		table = data.sheets()[i]  # 对应的获取 工作表的内容
		# 获取第2列的温度的数据，并且求平均温度，平均人数，以及异常的人数(温度>=37.4)
		temp_value = table.col_values(colx=1, start_rowx=1)  # 把标题除外了
		temp_ndarray = np.array(temp_value)
		abnormal = np.argwhere(temp_ndarray >= 37.4)
		# 判断是否为空的工作表
		if table.nrows == 0: continue
		# 每日的汇总统计
		now_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 把datetime转变为字符串
		result = '备注:\n 时间：{}\n总进出人数:{}\n异常人数:{}\n平均温度:{}'.format(now_time, len(temp_value), len(abnormal),
		                                                          np.mean(temp_ndarray))
		# print(now_time)
		row_index = len(temp_value) + 2  # 与数据空 两行的位置
		col_index = 0
		wokrsheet = wb.get_sheet(i)  # 访问当前的工作表 然后进行操作
		# 合并单元表，并且把result写在下面
		wokrsheet.write_merge(row_index, row_index + 1, col_index, 2, result)

		# 将异常人的这一行信息都变为高亮
		# 高亮的格式
		style = xlwt.XFStyle()
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
		pattern.pattern_fore_colour = 5
		# 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow,
		style.pattern = pattern

		# 首先要获取异常人的所有信息
		time_list = []
		for j in abnormal:
			rown = j[0]  # 行
			for col in range(table.ncols):  # table.ncols 工作表的列数
				content = table.cell_value(rown + 1, col)  # 把要标题算上

				if col == 2:
					# style.num_format_str = 'M/D/YY'      # 第二列的时候才是时间的格式
					# wokrsheet.write(rown + 1, col,content,style)
					# style.num_format_str = ''
					time_list.append((content, (rown + 1, col)))
				else:
					wokrsheet.write(rown + 1, col, content, style)

		# style.num_format_str = 'M/D/YY'  时间的格式会导致 数字显示不正常

		style.num_format_str = 'M/D/YY'
		for t in time_list:
			wokrsheet.write(t[1][0], t[1][1], t[0], style)

	wb.save(save_path)

def post_excel_email(excel_path,email_content,email_title):
	# 发信服务器
	smtp_server = 'smtp.qq.com'

	# 发信方的信息：发信邮箱，QQ邮箱授权码  # 不需要你QQ邮箱的密码,需要授权码就行
	from_addr = '919762350@qq.com'
	password = 'jjtrwaudfrgebbgj'

	# 收信方邮箱
	to_addr = '919762350@qq.com'
	msg = MIMEMultipart()
	msg.attach(MIMEText(email_content, 'plain', 'utf-8'))  # 放入邮箱的正文

	# 创建邮箱的附件

	# 读取本地的文件内容;构造附件
	att = MIMEText(open(excel_path, 'rb').read(), 'based64', 'utf-8')
	att['Content-Type'] = 'application/octet-stream'
	att['Content-Disposition'] = 'attachment; filename = "day_report.xls"'

	# 在把附件附上去
	msg.attach(att)

	# 邮件头信息
	msg['From'] = Header(from_addr)
	msg['To'] = Header(to_addr)
	msg['Subject'] = Header(email_title)

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


if __name__=='__main__':
	source_xls = '楼宇安防.xls'
	save_path ='楼宇安防_日报.xls'
	excel_path = save_path
	email_content = '国贸大厦今日统计的进出人数以及温度情况。详细内容见附件'
	email_title = '日报'
	get_excel(source_xls,save_path)
	# 发送邮箱 ，包含附件
	post_excel_email(excel_path, email_content, email_title)
