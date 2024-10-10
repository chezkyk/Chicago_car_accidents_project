from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['chicago_accidents']
accident_collection = db['accidents']