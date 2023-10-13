import sqlite3
conn = sqlite3.connect('Medicine_Data.db')  # Replace with your database file path
cursor = conn.cursor()
q1="create table Medicine(id int)"
cursor.execute(q1)  # Replace with your table name
data = cursor.fetchall()
conn.close()