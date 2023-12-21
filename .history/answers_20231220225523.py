from pymongo import MongoClient

# Connect to your MongoDB database
client = MongoClient('your_mongodb_connection_string')
db = client['Boof']
collection = db['your_collection']

# Example: Fetching context from the database
def fetch_context(question):
    # You'll need to implement a method to fetch relevant context based on the question
    # This is a placeholder for demonstration purposes
    return "Relevant context from the database"

# Using the model with database context
question = "Who wrote the Book of Mormon?"
context = fetch_context(question)
answer = qa_pipeline(question=question, context=context)
print(answer)
