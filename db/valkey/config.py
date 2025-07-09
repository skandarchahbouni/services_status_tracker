import redis
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

VALKEY_PASSWORD = os.getenv("VALKEY_PASSWORD")

# Connect to Redis
valkey_client = redis.Redis(host='localhost', port=6379, db=0, password=VALKEY_PASSWORD, decode_responses=True)