import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="julian",
        password="1234",
        database="fixture"
    )

