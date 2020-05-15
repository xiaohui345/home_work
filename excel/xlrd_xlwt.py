# -*- coding: utf-8 -*-
# @Author: 曾辉
import xlwt
import xlrd


source_xls = ['楼宇安防.xls']

data = []

for xls in source_xls:
	wb = xlrd.open_workbook(xls,formatting_info=True) #保留原xls的格式
	# print(wb.sheets()[0].row_values(0))
	for sheet in wb.sheets():
		for rownum in range(sheet.nrows):  # 读取所有的行的内容信息
			data.append(sheet.row_values(rownum))   # 读取的是内容 没有读取格式
			# sheet.row_values(rownum) 读取出来的数据是一个列表

print(data)
#
wk = xlwt.Workbook(encoding = 'utf-8')
worksheet  = wk.add_sheet('国贸写字楼')

# 时间格式
style = xlwt.XFStyle()
style.num_format_str = 'M/D/YY'
font = xlwt.Font()
# 加粗
bold_style = xlwt.XFStyle()
font.bold = True
style = xlwt.XFStyle()
bold_style.font = font
# 高亮的格式
gaoliang_style = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern.pattern_fore_colour = 5
# 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow,
gaoliang_style.pattern = pattern


for i in range(len(data)):
	# 每一行
	for j in range(len(data[i])):
		#每一行的每一列数据
		# 时间的格式
		# 自己还要配置格式
		if j == 2:
			worksheet.write(i, j, data[i][j],style)
		elif i == 4 :
			worksheet.write(i, j, data[i][j],bold_style)
		elif j == 0 and 0< i < 3:
			worksheet.write(i, j, data[i][j],gaoliang_style)
		else:
			worksheet.write(i,j,data[i][j])   # write 是从0开始的

wk.save('楼宇安防4_copy.xls')
