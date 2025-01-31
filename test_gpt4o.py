import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=API_KEY)

# Function to test GPT-4o Mini
def chat_with_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use GPT-4o Mini for cost efficiency
        messages=[{"role": "system", "content": "You are an AI created by Luca, now being integrated into a real-world system."},
                  {"role": "user", "content": prompt}],
        max_tokens=150  # Keep responses short to save tokens
    )
    return response.choices[0].message.content

# Run a test
if __name__ == "__main__":
    user_input = input("Ask something: ")
    response = chat_with_ai(user_input)
    print("AI Response:", response)