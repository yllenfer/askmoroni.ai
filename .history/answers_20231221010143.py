from pymongo import MongoClient
from transformers import pipeline
import spacy

nlp = spacy.load("en_core_web_sm")

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
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")


def get_answer(question, context):
    return qa_pipeline(question=question, context=context)



def fetch_context(question):
    # Analyze the question
    doc = nlp(question)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"]]  # Include verbs

    # Create a search query using extracted keywords
    search_query = " ".join(keywords)

    # Debugging: Print the search query
    print(f"Search Query: {search_query}")

    # Perform text search in MongoDB
    search_result = collection.find_one({"$text": {"$search": search_query}})
    
       # Fetch a broader range of text
    search_results = collection.find({"$text": {"$search": search_query}}).limit(5)  # Adjust limit as needed

    if search_results:
        combined_verses = " ".join([verse for doc in search_results for verse in doc['verses']])
        return combined_verses

    return "No relevant context found in the database."


# def extract_keywords(question):
#     # ... existing NLP-based extraction ...
#     # Add logic to handle different types of questions or implement NER
#     return keywords




while True:
    user_question = input("Ask a question about the Book of Mormon (type 'exit' to quit): ")
    
    if user_question.lower() == 'exit':
        break

    context = fetch_context(user_question)
    answer = get_answer(user_question, context)
    print(f"Answer: {answer['answer']}\n")
