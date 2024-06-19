import sqlite3

# 查看用户名
conn = sqlite3.connect('test2222.db')
c = conn.cursor()
print ("数据库打开成功")

cursor = c.execute("SELECT *  from user2")

for row in cursor:
    print("name = ", row[0])
    print("url = ", row[1])
    print("name = ", row[2],)
    print("pw = ", row[3],"\n")

print ("数据操作成功")

conn.close()