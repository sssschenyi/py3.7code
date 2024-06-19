import pandas as pd
import os
# 从excel 读取数据
add = os.getcwd()
print(add)
# df = pd.read_csv('Chrome 密码.csv', encoding = 'gb2312')
df = pd.read_csv('MicrosoftEdge密码.csv', encoding = 'utf-8')
print(df)
df1 = pd.read_excel('ctl.xls', sheet_name = None)
print(df1.keys())# 读取表单名
# df2 = pd.read_excel('ctl.xls', sheet_name = 'Sheet6')
# print(df2)

# 从 sql 数据库读取数据
import sqlite3
conn = sqlite3.connect('test2222.db')
# cursor = conn.cursor() # 开始数据库游标
# cursor.execute("CREATE TABLE userinfo (name TEXT, age INTEGER)")
# cursor.execute("INSERT INTO userinfo (name, age) VALUES ('Alice', 20)")
# cursor.execute("INSERT INTO userinfo (name, age) VALUES ('Bob', 30)")
# cursor.execute("INSERT INTO userinfo (name, age) VALUES ('Charlie', 40)")
# conn.commit() # 提交数据到数据库
df = pd.read_sql('select * from userinfo', conn)
# print(df)
# print(df.duplicated())
# print(df.head(3))
# 写入数据
# import xlwt

data = {'A': [1, 21, 2, 2, 3,2],'B': ['a', 'a', 'b', 'b', 'c', 'b']}
df = pd.DataFrame(data)
duplicated = df.duplicated()
# print(duplicated)


# 从 HTML 页面中读取数据
# url = 'https://www.runoob.com'
# dfs = pd.read_html(url)
# df = dfs[0] # 选择第一个数据框
