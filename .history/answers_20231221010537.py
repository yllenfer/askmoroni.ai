from pymongo import MongoClient
from transformers import pipeline
import spacy

nlp = spacy.load("en_core_web_sm")

# MongoDB connection
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client['bookOfMormonDB']
collection = db['chapters']

# Load QA model
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

def fetch_context(question):
    # Enhanced keyword extraction
    doc = nlp(question)
    keywords = " ".join([token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"]])

    print(f"Search Query: {keywords}")

    # Retrieve more comprehensive context
    search_results = collection.find({"$text": {"$search": keywords}}).limit(5)  # Adjust as needed
    combined_verses = ""
    for doc in search_results:
        combined_verses += " ".join(doc['verses'])
    return combined_verses if combined_verses else "No relevant context found in the database."

while True:
    user_question = input("Ask a question about the Book of Mormon (type 'exit' to quit): ")
    if user_question.lower() == 'exit':
        break

    context = fetch_context(user_question)
    answer = qa_pipeline(question=user_question, context=context)
    print(f"Answer: {answer['answer']}\n")
