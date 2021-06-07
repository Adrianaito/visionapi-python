import mysql.connector

# to connect with database
mydb = mysql.connector.connect(
    host='localhost', user='chouri', passwd='123123123', database='')

mycursor = mydb.cursor()

mycursor.execute("select * from ...")

for i in mycursor:
    print(i)
