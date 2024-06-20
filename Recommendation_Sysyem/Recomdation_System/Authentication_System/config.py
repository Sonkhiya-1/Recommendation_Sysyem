import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'AuthDB')
    MYSQL_USER = os.getenv('MYSQL_USER', 'recomdation')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Happy@123')

    @staticmethod
    def get_mysql_connection_params():
        return {
            'host': Config.MYSQL_HOST,
            'database': Config.MYSQL_DATABASE,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD
        }
