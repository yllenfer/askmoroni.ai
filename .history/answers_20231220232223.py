from pymongo import MongoClient
from transformers import pipeline

# Load a pre-trained question-answering model
qa_pipeline = pipeline("question-answering")

# Connect to your MongoDB database
client = MongoClient('your_mongodb_connection_string')
db = client['bookOfMormonDB']
collection = db['chapters']

def fetch_context(question):
    # Basic keyword extraction from the question
    keywords = question.split()

    # Search the database for these keywords and fetch relevant text
    for keyword in keywords:
        chapter = collection.find_one({"text": {"$regex": keyword, "$options": "i"}})
        if chapter:
            return chapter['text']

    return "No relevant context found in the database."

while True:
    # User inputs the question
    user_question = input("Ask a question about the Book of Mormon (type 'exit' to quit): ")
    
    if user_question.lower() == 'exit':
        break

    # Fetch context from the database
    context = fetch_context(user_question)

    # Get the answer from the model
    answer = qa_pipeline(question=user_question, context=context)
    print(f"Answer: {answer['answer']}\n")
