import mysql.connector

PORT = 8000

def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database="byee_database"
    )
    return connection