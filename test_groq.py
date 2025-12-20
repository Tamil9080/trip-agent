import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key length: {len(api_key)}")
    print(f"API Key start: {api_key[:4]}...")

if not api_key:
    print("Please set GROQ_API_KEY in .env file")
    exit()

client = Groq(api_key=api_key)

prompt = """
Generate a list of 3 distinct tourist activities for Paris.
Return the response ONLY as a valid JSON object with a key "activities".
"""

try:
    print("Sending request to Groq...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful travel assistant that outputs only valid JSON."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
    )
    
    response_content = chat_completion.choices[0].message.content
    print("\nResponse received:")
    print(response_content)
    
    data = json.loads(response_content)
    print("\nJSON parsed successfully.")
    
except Exception as e:
    print(f"\nError occurred: {e}")
