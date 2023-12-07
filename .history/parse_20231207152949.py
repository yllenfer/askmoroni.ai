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


