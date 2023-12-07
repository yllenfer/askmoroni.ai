import re
import json

def parse_book_of_mormon(text):
    chapter_pattern = re.compile(r'Chapter (\d+)')
    verse