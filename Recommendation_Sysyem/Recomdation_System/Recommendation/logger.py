import logging
from config import load_config

config = load_config()
log_level = config['logging']['level']
log_file = config['logging']['file']

logging.basicConfig(
    level=getattr(logging, log_level.upper(), None),
    filename=log_file,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
