from pymongo import MongoClient
from config import *
client = MongoClient(MONGO_URI)

db = client[DB_NAME]

month_collection = db[COLLECTION_NAMES[0]]
week_collection = db[COLLECTION_NAMES[1]]
day_collection= db[COLLECTION_NAMES[2]]
