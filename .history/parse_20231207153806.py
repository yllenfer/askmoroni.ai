import re
import json

def parse_book_of_mormon(text):
    chapter_pattern = re.compile(r'Chapter (\d+)')
    verse_pattern = re.compile(r'\d+') 
    book = {}
    current_chapter = None
    current_verse = None
    for line in text.slit('\n'):
        if chapter_pattern.match(line):
            current_chapter = line
            book[current_chapter] = []
        elif current_chapter and verse_pattern.match(line.strip()):
            book[current_chapter].append(line.strip())
    return book


parse_book_of_mormon(text)
with open('thebookofmormon.txt', 'w') as f:
    json.dump(book, f)


Use the parse_book_of_mormon function on my thebookofmormon.txt file and save the result to a variable called book. Then, use the json.dump function to save the book variable to a file called thebookofmormon.json.

# Path: parse.py
import re
import json
