import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="food",
        password="food",
        database="food_recommendation"
    )
