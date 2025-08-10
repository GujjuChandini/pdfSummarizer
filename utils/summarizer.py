import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() # Load GEMINI_API_KEY from .env

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in your .env file.")
    print("Please make sure your .env file exists and contains GEMINI_API_KEY=YOUR_KEY_HERE")
    # You might want to exit here if the API key is essential
    exit()

genai.configure(api_key=api_key)

# IMPORTANT: Changed from "gemini-pro" to "gemini-1.5-pro"
# Based on your check_models.py output, this model is available.
# Be aware of potential costs associated with using this model.
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Optional: Test if the model is reachable
    # print(model.count_tokens("Hello, world!"))
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    print("Please ensure your API key is valid and the model name is correct for your region/account.")
    exit()


def summarize_chunk(chunk):
    prompt = (
        "Summarize the following academic text into exactly 5 bullet points. "
        "List them from most important to least important:\n\n"
        f"{chunk}"
    )

    try:
        response = model.generate_content(prompt, request_options={"timeout": 60}) # Added a timeout
        return response.text.strip()
    except Exception as e:
        print(f"Error during Gemini content generation: {e}")
        # If there's an error from the API, return a placeholder or re-raise
        return "ERROR: Could not summarize this chunk due to an API error."