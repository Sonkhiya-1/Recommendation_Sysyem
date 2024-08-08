import logging
import os
from dotenv import load_dotenv
from server.server import Server

load_dotenv()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("server.log"),
            logging.StreamHandler()
        ]
    )

    server_config = {
        'host': os.getenv("HOST"),
        'port': int(os.getenv("PORT"))
    }

    Server(server_config['host'], server_config['port'])