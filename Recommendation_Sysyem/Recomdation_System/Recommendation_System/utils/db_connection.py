import mysql.connector
import logging

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="jinwoo",
            password="Arise",
            database="food_recommend"
        )
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to the database: {err}")
        return None
