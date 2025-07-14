from redis.sentinel import Sentinel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the comma-separated IP addresses from the environment variable
SENTINELS = os.getenv("SENTINELS")

# Split the IP addresses into a list
ip_list = SENTINELS.split(',')

VALKEY_PASSWORD = os.getenv("VALKEY_PASSWORD")

# Connect to Sentinel(s) using the IP addresses
sentinel = Sentinel([(ip, 26379) for ip in ip_list], socket_timeout=0.5)

# Get a connection to the master (write operations)
valkey_client = sentinel.master_for('mymaster', socket_timeout=0.5, password=VALKEY_PASSWORD, db=0, decode_responses=True)