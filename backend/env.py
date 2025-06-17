import os
from dotenv import load_dotenv
    
r = load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'), override=True)

debug = os.getenv('DEBUG') == '1'
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_db = os.getenv('POSTGRES_DB')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
qwen_enabled = os.getenv('QWEN_ENABLED') == '1'
biobert_enabled = os.getenv('BIOBERT_ENABLED') == '1'

import logging
import colorlog

logger = logging.getLogger("uvicorn")

# Logger
if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s%(reset)s:\t%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    reset=True
)
for handler in logger.handlers:
    handler.setFormatter(formatter)