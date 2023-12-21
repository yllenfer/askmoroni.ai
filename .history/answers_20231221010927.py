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
    # Analyze the question
    doc = nlp(question)
    keywords = " ".join([token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"]])

    print(f"Search Query: {keywords}")

    # Search for the chapter containing the keywords
    search_result = collection.find_one({"$text": {"$search": keywords}})
    
    if search_result:
        # Combine all verses from the found chapter
        full_chapter_text = " ".join(search_result['verses'])
        return full_chapter_text

    return "No relevant context found in the database."


while True:
    user_question = input("Ask a question about the Book of Mormon (type 'exit' to quit): ")
    if user_question.lower() == 'exit':
        break

    context = fetch_context(user_question)
    answer = qa_pipeline(question=user_question, context=context)
    print(f"Answer: {answer['answer']}\n")