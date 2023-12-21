from pymongo import MongoClient
from transformers import pipeline

# Replace with your actual MongoDB connection string
connection_string = "mongodb://localhost:27017"

try:
    # Connect to your MongoDB database
    client = MongoClient(connection_string)
    # This line checks if the server is available
    client.admin.command('ping')
    print("Connected to MongoDB:", client.list_database_names())
    
    db = client['bookOfMormonDB']
    collection = db['chapters']

except Exception as e:
    print("Unable to connect to the server:", e)
    exit()  # Exit if the connection is not successful

# Load a pre-trained question-answering model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


def fetch_context(question):
    keywords = question.split()

    for keyword in keywords:
        # Search within the verses array
        result = collection.find_one({"verses": {"$regex": keyword, "$options": "i"}})
        if result:
            # Concatenate the verses array into a single string for context
            context = ' '.join(result['verses'])
            return context

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
