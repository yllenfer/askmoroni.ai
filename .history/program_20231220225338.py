from transformers import pipeline

# Load a pre-trained question-answering model
qa_pipeline = pipeline("question-answering")


context = "The Book of Mormon is another testament of Jesus Christ. It was written by ancient prophets."
question = "What is the Book of Mormon?"

answer = qa_pipeline(question=question, context=context)
print(answer)
