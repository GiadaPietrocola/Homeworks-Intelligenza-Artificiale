import string
import re
from distutils.command.clean import clean



def clean_text(text: str) -> str:

    text = text.translate(str.maketrans('', '', string.punctuation))
    text = " ".join(text.split())
    return text.lower()

def count_words(text: str) -> dict:

    words=clean_text(text).split()

    return {word: words.count(word) for word in set(words)}


def find_longest_word(text: str) -> str:

    if text == "":
        print("Il testo è vuoto, impossibile trovare parola più lunga")
        return ""

    words = clean_text(text).split()
    return max(words, key=len)


def format_sentences(text: str) -> list:

    sentences = re.split(r'[.!?]', text)
    formatted_sentences = [sentence.strip().capitalize() for sentence in sentences if sentence.strip()]
    return formatted_sentences