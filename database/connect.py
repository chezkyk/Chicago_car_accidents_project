from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['chicago_accidents']

month_collection = db['monthly']
week_collection = db['weekly']
day_collection= db['daily']
