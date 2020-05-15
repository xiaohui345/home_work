# -*- coding: utf-8 -*-
# @Author: 曾辉
import xlwt
import xlrd
import numpy as np
import datetime
from xlutils.copy import copy

source_xls = '楼宇安防.xls'

data = xlrd.open_workbook(source_xls)


# 创建一个新的工作簿
wb = xlwt.Workbook()
# 把读取到的工作簿的内容全部复制到 新的工作簿上
wb = copy(data)


for i in range(len(data.sheets())):
	table = data.sheets()[i]  # 对应的获取 工作表的内容
	#获取第2列的温度的数据，并且求平均温度，平均人数，以及异常的人数(温度>=37.4)
	temp_value = table.col_values(colx=1,start_rowx=1)  # 把标题除外了
	temp_ndarray = np.array(temp_value)
	abnormal = np.argwhere(temp_ndarray>=37.4)
	# [[0]
	#  [2]
	#  [6]
	#  [8]]
	# 返回True结果的Index  是嵌套的
	# print(temp_ndarray)
	# print(abnormal)
	# 判断是否为空的工作表
	if table.nrows == 0:continue
	# 每日的汇总统计
	now_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 把datetime转变为字符串
	result = '备注:\n 时间：{}\n总进出人数:{}\n异常人数:{}\n平均温度:{}'.format(now_time,len(temp_value),len(abnormal),np.mean(temp_ndarray))
	# print(now_time)
	row_index = len(temp_value)+2  # 与数据空 两行的位置
	col_index = 0
	wokrsheet = wb.get_sheet(i)  # 访问当前的工作表 然后进行操作
	#合并单元表，并且把result写在下面
	wokrsheet.write_merge(row_index, row_index+1,col_index, 2, result)

	# 将异常人的这一行信息都变为高亮
	# 高亮的格式
	style = xlwt.XFStyle()
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern.pattern_fore_colour = 5
	# 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow,
	style.pattern = pattern

	# 首先要获取异常人的所有信息
	time_list=[]
	for j in abnormal:
		rown = j[0]  # 行
		for col in range(table.ncols):  #table.ncols 工作表的列数
			content = table.cell_value(rown+1,col)    # 把要标题算上

			if col ==2:
				# style.num_format_str = 'M/D/YY'      # 第二列的时候才是时间的格式
				# wokrsheet.write(rown + 1, col,content,style)
				# style.num_format_str = ''
				time_list.append((content,(rown + 1,col)))
			else:
				wokrsheet.write(rown + 1, col, content,style)

	# style.num_format_str = 'M/D/YY'  时间的格式会导致 数字显示不正常

	style.num_format_str = 'M/D/YY'
	for t in time_list:
		wokrsheet.write(t[1][0], t[1][1], t[0], style)

wb.save('楼宇安防_日报.xls')