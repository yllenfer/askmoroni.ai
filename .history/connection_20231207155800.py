import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.BookofMormonDB
collection = db.askMoroni

with open('parsed_book_of_mormon.json', 'r', encoding='utf-8') as f:
    parsed_book = json.load(f)