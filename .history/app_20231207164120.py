from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client.bookOfMormonDB

@app.route('/')
def home():
    return "Welcome to the Book of Mormon API!"

if __name__ == '__main__':
    app.run(debug=True)
