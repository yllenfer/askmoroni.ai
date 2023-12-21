from pymongo import MongoClient
from transformers import pipeline

# Load a pre-trained question-answering model
qa_pipeline = pipeline("question-answering")


context = "The Book of Mormon is another testament of Jesus Christ. It was written by ancient prophets."
question = "What is the Book of Mormon?"

answer = qa_pipeline(question=question, context=context)
print(answer)


# Connect to your MongoDB database
client = MongoClient('your_mongodb_connection_string')
db = client['bookOfMormonDB']
collection = db['chapters']

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
