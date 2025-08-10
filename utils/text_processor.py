import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    return text.strip()

def chunk_text(text, max_words=400):
    words = text.split()
    chunks = []

    # Iterate through the words, taking 'max_words' at a time
    for i in range(0, len(words), max_words):
        chunk = ' '.join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks