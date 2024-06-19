import sqlite3
import time

# 一个简单的数据插入计算器
# 开始时间
starttime = time.time()

conn = sqlite3.connect('test2222.db')
print ("数据库打开成功")
# cursor = c.execute("CREATE TABLE test (i INTEGER)")
cursor = conn.cursor() # 开始数据库游标

s = 1000000
for i in range(s):
    cursor.execute("INSERT INTO test (i) VALUES ({})".format(i))
conn.commit() # 提交数据到数据库

# 结束时间
endtime = time.time() - starttime
print ("数据操作成功,插入{}条数据，用时:{}".format(s, endtime))
conn.close()