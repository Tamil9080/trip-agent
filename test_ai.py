import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")

if not api_key:
    print("Please set GEMINI_API_KEY in .env file")
    exit()

genai.configure(api_key=api_key)

try:
    print("Attempting to list models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")

    print("\nAttempting to generate content with 'gemini-2.0-flash'...")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello, are you working?")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"\nError occurred: {e}")
