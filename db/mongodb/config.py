from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load environment variables
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

# Initialize the database and collections
db = client["history"]
services_status_collection = db["services_status"]
