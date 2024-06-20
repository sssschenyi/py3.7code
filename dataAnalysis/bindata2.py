import sqlite3
import time
import random


# 一个简单的数据插入计算器
# 开始时间
starttime = time.time()

conn = sqlite3.connect('test2222.db')
print ("数据库打开成功")
# cursor = c.execute("CREATE TABLE test (i INTEGER)")
cursor = conn.cursor() # 开始数据库游标
# 开始事务，用于大量插入数据
cursor.execute("BEGIN TRANSACTION")
s = 100
# values = []
# 利用推导式生成列表
values1 = [(random.randint(1,s),) for x in range(0, s)] # 批量插入要注意格式,例如(i,)
"""
# 利用for循环生成列表
for i in range(s):
    value = random.randint(1, 1000)
    values.append((value,))
# """
# print(values1)xit
# 批量插入数据
cursor.executemany("INSERT INTO test (i) VALUES (?)",values1)
# 提交事务
conn.execute('commit')

# 计算代码执行时间
endtime = time.time() - starttime
print ("数据操作成功,插入{}条数据，用时:{}".format(s, endtime))
conn.close()
