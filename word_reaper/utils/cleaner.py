import re
import unicodedata
from tqdm import tqdm

def clean_words(word_list):
    """
    Normalize and clean a list of words:
    - Convert to lowercase
    - Remove special characters
    - Remove diacritics
    - Strip whitespace
    - Remove duplicates
    """
    cleaned = set()

    for word in tqdm(word_list, desc="Cleaning words", unit="word"):
        # Normalize and remove diacritics
        word = unicodedata.normalize('NFKD', word)
        word = ''.join([c for c in word if not unicodedata.combining(c)])
        
        # Convert to lowercase
        word = word.lower()
        
        # Remove special characters (keep letters and numbers)
        word = re.sub(r'[^a-z0-9]', '', word)

        if word:
            cleaned.add(word)

    return sorted(cleaned)
