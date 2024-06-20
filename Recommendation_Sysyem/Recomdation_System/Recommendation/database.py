import mysql.connector
from config import load_config

def get_db_connection():
    config = load_config()
    return mysql.connector.connect(
        host=config['database']['host'],
        user=config['database']['user'],
        password=config['database']['password'],
        database=config['database']['database']
    )
