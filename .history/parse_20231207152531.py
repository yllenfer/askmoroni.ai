import re
import json

def parse_book_of_mormon(text):
    chapter_pattern = re.compile(r'Chapter (\d+)')
    verse_pattern = re.compile(r'\d+') 
    book = {}
    current_chapter = None
    current_verse = None
    for line in text.slit('\n') 