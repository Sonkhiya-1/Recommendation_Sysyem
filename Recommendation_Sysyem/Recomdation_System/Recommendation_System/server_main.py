import logging
from server.server import Server

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("server.log"),
                            logging.StreamHandler()
                        ])
    server_config = {
        'host': 'localhost',
        'port': 12346
    }
    Server(server_config['host'], server_config['port'])