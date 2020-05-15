# 写入 楼宇安防.xls
import xlwt

# 创建一个workbook 工作簿 设置编码
workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet 工作表
worksheet = workbook.add_sheet('国贸写字楼')

# 写入excel，参数对应 行, 列, 值
worksheet.write(0, 0, label = '人员')
# 保存文件
# workbook.save('./楼宇安防demo.xls')


""" 设置字体样式 """
# 初始化样式
style = xlwt.XFStyle() 
# 为样式创建字体
font = xlwt.Font() 
font.name = 'Times New Roman' 
# 加粗
font.bold = True 
# 下划线
font.underline = True 
# 斜体字
font.italic = True 
# 设定样式
style.font = font 
worksheet.write(0, 1, '体温', style) # 带样式的写入
# workbook.save('楼宇安防2.xls')


""" 设置单元格宽度 """
#worksheet = workbook.add_sheet('世贸天阶')
worksheet.write(0, 2,'时间')
# 设置单元格宽度
worksheet.col(0).width = 3333
# workbook.save('./楼宇安防2.xls')


""" 添加日期到单元格 """
import datetime
# 获取样式
style = xlwt.XFStyle()
# Other options: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
style.num_format_str = 'M/D/YY'
worksheet.write(1, 2, datetime.datetime.now(), style)
worksheet.write(2, 2, datetime.datetime.now(), style)
# workbook.save('楼宇安防demo.xls')

# """ 向单元格添加一个公式 """
worksheet.write(1, 1, 37.4)
worksheet.write(2, 1, 36.5)
# # 求两个单元格的平均值
worksheet.write(3, 1, xlwt.Formula('AVERAGE(B2,B3)'))
workbook.save('楼宇安防3.xls')


""" 向单元格添加一个链接 """
# worksheet.write(1, 3, xlwt.Formula('HYPERLINK("http://www.baidu.com";"baidu")'))
# workbook.save('楼宇安防2.xls')

""" 合并列和行 """
# write_merge(行开始, 行结束，列开始, 列结束, '数据内容')
# 创建字体
font = xlwt.Font()
# 加粗
font.bold = True
style = xlwt.XFStyle()
style.font = font
worksheet.write_merge(4, 5, 0, 2, '备注：需要检查是否佩戴口罩', style)
# workbook.save('楼宇安防2.xls')

""" 给单元格添加边框和背景色 """
# 边框样式
borders = xlwt.Borders()
borders.left = 2
borders.right = 2
borders.top = 2
borders.bottom = 2
# 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
# 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13

borders.left_colour = 0x40
borders.right_colour = 0x40
borders.top_colour = 0x40
borders.bottom_colour = 0x40
# 创建样式
style = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern.pattern_fore_colour = 5
# 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow,
style.pattern = pattern
style.borders = borders
worksheet.write(1, 0, '张飞', style)
worksheet.write(2, 0, '关羽', style)

# workbook.save('楼宇安防4.xls')


import xlrd
# formatting_info=True 读取excel 的时候保留格式
# data = xlrd.open_workbook('./楼宇安防.xls')
#
# table = data.sheets()[0]
#
# print(table.cell_value(1, 1))
# print(table.cell(0, 1))


#在原有数据上的excel上添加内容的话 就是先 创建一个工作簿 然后创建一个工作表 读取原excel上的所有内容。
# 然后在添加到工作表上去，在新的工作表上添加内容，然后保存

