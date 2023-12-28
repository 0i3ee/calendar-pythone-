import mysql.connector

def connect():
    con = mysql.connector.connect(host="localhost", user="root", password="", database="calendra_event")
    return con

def get_cursor(con):
    cursor = con.cursor()
    return cursor

def close_cursor(cursor):
    cursor.close()

def close_connection(con):
    if con.is_connected():
        con.close()
