import sqlite3
import csv

connection = sqlite3.connect("Timetable2.db")
cursor = connection.cursor()

with open('data1.csv', 'r') as file:
    no_records = 0
    for row in file:
        cursor.execute("INSERT INTO Timetable2 VALUES (?,?,?,?,?,?,?,?)", row.split(","))
        connection.commit()
        no_records = no_records + 1

connection.close()

print('\n {} Records Transferred'.format(no_records))

