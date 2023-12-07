from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client.bookOfMormonDB

@app.route('/')
def home():
    return "Welcome to the Book of Mormon API!"


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')  # Get the query parameter from the URL
    results = db.chapters.find({"$text": {"$search": query}})  # Text search in MongoDB
    response = [{"chapter": result["chapter"], "verses": result["verses"]} for result in results]
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
