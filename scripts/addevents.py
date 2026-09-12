import sys
import mysql.connector
from mysql.connector import Error
import dbfunc
conn = dbfunc.getConnection()   #connection to DB
DB_NAME = 'mydb'             #DB Name
TABLE_NAME = 'Events'

INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
    idEvents, EventsName, EventsDescription) VALUES (%s, %s, %s);' 

idEvents = input("Enter Event ID: ")
EventsName = input("Enter Event Name: ")
EventsDescription = input("Enter Event Description: ")

cursor = conn.cursor()
try:
    cursor.execute(INSERT_statement, (idEvents, EventsName, EventsDescription))
    conn.commit()
    print("Event added successfully.")
except Error as e:
    print("Error occurred while adding event:", e)
finally:
    cursor.close()
    conn.close()