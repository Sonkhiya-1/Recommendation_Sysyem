import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="recommendation_system",
        password="Happy@123",  # Ensure this matches the password you set
        database="recommendation_system"
    )