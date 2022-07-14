import csv

import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="arpit", passwd="0122", database="face_recognisation")
mycursor = mydb.cursor()


with open('attendance.csv') as f:
    f = csv.reader(f, delimiter=',')
    all_value = []
    for row in f:
        value = (row[0],row[1])
        all_value.append(value)

query = "insert into `Attendance`(`Name` , `Time`) values (%s,%s)"
mycursor.execute("select * from Attendance")

for i in mycursor:
    print(i)
mycursor.executemany(query, all_value)
mydb.commit()
