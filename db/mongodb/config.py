from pymongo.mongo_client import MongoClient
import os


# Load environment variables
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

# Initialize the database and collections
db = client["history"]
services_status_collection = db["services_status"]
