import socket
import logging

def create_socket(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.settimeout(5)
        return s
    except Exception as e:
        logging.error(f"Failed to create socket: {e}")
        raise