import sqlite3 as sql 
from yijing import data

conn=sql.connect('I_Ching.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS I_Ching
                  (查阅码 TEXT PRIMARY KEY, 
                   辞 TEXT,
                   链接 TEXT)''')
# 准备插入数据的SQL语句
insert_sql = 'INSERT INTO I_Ching (查阅码, 辞, 链接) VALUES (?, ?, ?)'
for index, datas in data.items():
    ci = datas.get('辞')
    link = datas.get('链接')
    cursor.execute(insert_sql, (index, ci, link))
print("数据已成功存入数据库")
conn.commit()
print("数据库已提交")
conn.close()