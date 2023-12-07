from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

# Configure Flask-Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
limiter.init_app(app)

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client.bookOfMormonDB

@app.route('/search', methods=['GET'])
@limiter.limit("10 per minute")  # Specific rate limit for this route
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
                print("MongoDB error:", e)
    abort(500, description="Database error")
except Exception as e:
    print("General error:", e)
    abort(500, description="Server encountered an error")


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify(error=str(error)), 500

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="Rate limit exceeded", details=str(e.description)), 429

if __name__ == '__main__':
    app.run(debug=True)
