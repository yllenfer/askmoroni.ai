import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.bookOfMormonDB
collection = db.chapters

# Load JSON data
with open('book_of_mormon.json', 'r') as file:
    data = json.load(file)

# Insert data into the collection
for chapter, verses in data.items():
    document = {
        'chapter': chapter,
        'verses': verses
    }
    collection.insert_one(document)

print("Data uploaded successfully")
