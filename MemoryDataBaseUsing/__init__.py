from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')
REDIS_HOST = getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = getenv('REDIS_PORT', 6379)
