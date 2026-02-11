import mysql.connector
import json


connection = mysql.connector.connect(host="localhost",user="root",passwd="root1234",database="startersql")

cursor = connection.cursor(dictionary=True)
cursor.execute("select * from users")

rows = cursor.fetchall()
"""
print_json(json.dumps(rows ,indent=4, default=str))
"""

with open('users.json','w') as json_file:
    json_file.write(json.dumps(rows,indent=4, default=str))




cursor.close()
connection.close()













