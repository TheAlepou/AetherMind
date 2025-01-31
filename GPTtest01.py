import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = API_KEY

# Test function
def chat_with_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an AI created by Luca."},
                  {"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response["choices"][0]["message"]["content"]

# Run a test
if __name__ == "__main__":
    user_input = input("Ask something: ")
    response = chat_with_ai(user_input)
    print("AI Response:", response)