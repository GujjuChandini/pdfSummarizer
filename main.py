from dotenv import load_dotenv
load_dotenv()

import os
from utils.pdf_reader import extract_text_from_pdf
from utils.text_processor import clean_text, chunk_text
from utils.summarizer import summarize_chunk

while True:
    file_choice = input("Enter 'text' for input.txt or 'pdf' for sample.pdf: ").lower().strip()
    if file_choice == 'text':
        input_file_name = "input.txt"
        break
    elif file_choice == 'pdf':
        input_file_name = "sample.pdf"
        break
    else:
        print("Invalid choice. Please type 'text' or 'pdf'.")

input_file_path = os.path.join("inputs", input_file_name)

print(f"Reading text from {input_file_path}...")
raw_text = ""
try:
    os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
    
    if input_file_path.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(input_file_path)
    elif input_file_path.lower().endswith('.txt'):
        with open(input_file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        print("Error: Unsupported file type. Please use a .txt or .pdf file.")
        exit()
        
    print("Text read successfully.")
except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found. Please ensure it exists in the '{os.path.dirname(input_file_path)}' folder.")
    exit()
except Exception as e:
    print(f"Error reading input file '{input_file_path}': {e}")
    exit()

if not raw_text or not raw_text.strip():
    print("Error: The input file is empty or contains only whitespace. Please add some text.")
    exit()

print("Cleaning text...")
cleaned_text = clean_text(raw_text)
print("Text cleaned.")

print("Chunking text...")
chunks = chunk_text(cleaned_text, max_words=400)
print(f"Text split into {len(chunks)} chunks.")

summary_output = ""
print("Summarizing chunks using Gemini AI...")
for i, chunk in enumerate(chunks):
    try:
        summary = summarize_chunk(chunk)
        summary_output += f"\n--- Summary for Chunk {i+1} ---\n{summary}\n"
        print(f"  - Chunk {i+1} summarized successfully.")
    except Exception as e:
        summary_output += f"\n--- Error summarizing Chunk {i+1} ---\nError: {e}\n"
        print(f"  - Error summarizing Chunk {i+1}: {e}")

os.makedirs("outputs", exist_ok=True)
output_file_path = "outputs/summary.txt"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(summary_output)

print(f"\n✅ Summary process complete. Output saved to {output_file_path}")