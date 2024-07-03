import mysql.connector
import logging

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="food_user",
            password="Happy@123",
            database="recommendation_food"
        )
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to the database: {err}")
        return None
