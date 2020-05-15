"""
    提取完整表格
"""

import pdfplumber
import pandas as pd


filename = '2018高新认证名单.pdf'
with pdfplumber.open(filename) as pdf:
	# 创建一个空的DataFrame，然后再添加数据
	df = pd.DataFrame(columns=["ID", "企业名称"])
	for page in pdf.pages:  #pdf.pages 的所有的页数
		# page = pdf.pages[1]
		text = page.extract_text()  #提取内容
		print(text)
		table = page.extract_tables() # 提取表格
		for t in table:
			# 得到的table是嵌套list类型，转化成DataFrame类型，方便后续处理
			print(t)
			temp_df = pd.DataFrame(t[2:], columns=["ID", "企业名称"])
			print(temp_df)
			# df = df.append(temp_df)
			df = df.append(temp_df, ignore_index=True)  #循环的往后添加
		# df = pd.merge([df, temp_df])
		# print(df)
		break


# 保存文件
# df.to_csv('2018高新认证名单.csv', index=False)
