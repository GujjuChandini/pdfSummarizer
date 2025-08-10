import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() # Load GEMINI_API_KEY from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit()

genai.configure(api_key=GEMINI_API_KEY)

print("Available Gemini Models:")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(f"- {m.name} (Supports generateContent)")
    else:
        print(f"- {m.name}")