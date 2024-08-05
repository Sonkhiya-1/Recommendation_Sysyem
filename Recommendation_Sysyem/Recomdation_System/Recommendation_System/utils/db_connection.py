# server/utils/db_connection.py

import mysql.connector
import logging

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="fire",
            password="Arise",
            database="recommendation_new2"
        )
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to the database: {err}")
        return None
