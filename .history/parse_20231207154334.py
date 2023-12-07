import re
import json

def parse_book_of_mormon(text):
    chapter_pattern = re.compile(r'Chapter (\d+)')
    verse_pattern = re.compile(r'\d+') 
    book = {}
    current_chapter = None

    for line in text.split('\n'):
        if chapter_pattern.match(line):
            current_chapter = line
            book[current_chapter] = []
            print(f"Found chapter: {current_chapter}")  # Debugging print
        elif current_chapter and verse_pattern.match(line.strip()):
            book[current_chapter].append(line.strip())
            print(f"Added verse to {current_chapter}")  # Debugging print
    return book

# Read the text file with UTF-8 encoding
with open('thebookofmormon.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Parse the text
parsed_book = parse_book_of_mormon(text)

# Debugging print
print(f"Total chapters parsed: {len(parsed_book)}")

# Write the parsed data to a JSON file
with open('parsed_book_of_mormon.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_book, f)




