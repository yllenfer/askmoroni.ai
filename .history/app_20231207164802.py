from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from pymongo.errors import PyMongoError
app = Flask(__name__)

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client.bookOfMormonDB

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '')

        # Input validation
        if not query or len(query.strip()) == 0:
            abort(400, description="Invalid query parameter")

        # Text search in MongoDB
        results = db.chapters.find({"$text": {"$search": query}})
        response = [{"chapter": result["chapter"], "verses": result["verses"]} for result in results]
        return jsonify(response)

    except PyMongoError as e:
        # Log e details here for debugging
        abort(500, description="Database error")

    except Exception as e:
        # Log e details here for debugging
        abort(500, description="Server encountered an error")

@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify(error=str(error)), 500

if __name__ == '__main__':
    app.run(debug=True)
