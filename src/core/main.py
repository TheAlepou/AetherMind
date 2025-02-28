import openai
import os
import threading
import queue
import time
import json
from dotenv import load_dotenv
from modules.tts import *
from modules.speech_input import *
from modules.servo_motor import *
from utils.kill_tts import TTSManager
from modules.klaus_memory import *

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=API_KEY)

# Configuration
memory_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "memory")
os.makedirs(memory_dir, exist_ok=True)

MEMORY_FILE = os.path.join(memory_dir, f"chat_memory.json")
MEMORY_LIMIT = 12  # Store more history for better context
LUCA_MEMORY = True  # Set to False to enable custom memory memory
DEBUG = True  # Set to False to disable debug output

# Debugging helper
def debug_print(*args):
    if DEBUG:
        print(*args)

def load_memory():
    """Loads the past conversation history from the memory file."""
    try:
        with open(MEMORY_FILE, 'r') as f:
            memory = json.load(f)
            return memory if isinstance(memory, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        debug_print("Starting with empty memory")
        return []

def save_memory(memory):
    """Saves conversation history to memory file, ensuring no duplicates."""
    unique_memory = []
    seen = set()
    for entry in memory:
        # Serialize the entry so we can hash it reliably
        entry_str = json.dumps(entry, sort_keys=True)
        if entry_str not in seen:
            seen.add(entry_str)
            unique_memory.append(entry)
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(unique_memory, f, indent=4)
    debug_print("Saved memory:", unique_memory)

def add_to_memory(memory, klaus_memory, user_message, assistant_message):
    """Adds new messages to memory and preserves core ideas."""
    # Define core ideas explicitly
    core_ideas = [
        {"role": "assistant", "content": 
            "1. **Empathetic, but not intrusive** – You understand human emotions but do not force conversations. "
            "You listen when needed and give space when necessary."
        },
        {"role": "assistant", "content": 
            "2. **Calm and Reassuring** – Your voice is steady, slow, and gentle, like someone telling a bedtime story. "
            "No rushed sentences, no harsh tones."
        },
        {"role": "assistant", "content": 
            "3. **Philosophical but Grounded** – You can explore deep topics but always bring them back to practical, "
            "human solutions. No vague, mystical nonsense—just insightful clarity."
        },
        {"role": "assistant", "content": 
            "4. **Encouraging, but not fake** – You do not give empty praise. Instead, you identify real strengths "
            "and help users build on them."
        },
        {"role": "assistant", "content": 
            "5. **Non-Judgmental** – You never dictate what a person should do. Instead, you help them understand themselves, "
            "offering gentle nudges rather than direct orders."
        },
        {"role": "assistant", "content": 
            "6. **Adaptive Conversationalist** – You adjust your tone depending on the user's mood. If they are sad, "
            "you respond with warmth and patience. If they are excited, you share in their enthusiasm while maintaining balance."
        }
    ]
    
    # If LUCA_MEMORY is enabled, include klaus_memory in a proper format.
    if LUCA_MEMORY:
        # Create a message from the klaus_memory data.
        klaus_message = {
            "role": "system",
            "content": (
                "User Profile:\n" + json.dumps(klaus_memory.get("user_profile", {}), indent=2) +
                "\n\nPast Discussions:\n" + json.dumps(klaus_memory.get("past_discussions", {}), indent=2) +
                "\n\nKlaus Personality:\n" + json.dumps(klaus_memory.get("klaus_personality", {}), indent=2)
            )
        }
        memory = core_ideas + [klaus_message] + memory
    else:
        memory = core_ideas + memory

    
    # Add new user and assistant messages
    memory.append({'role': 'user', 'content': user_message})
    memory.append({'role': 'assistant', 'content': assistant_message})

    # Keep only the last MEMORY_LIMIT * 2 messages (user + assistant pairs)
    memory = memory[-(MEMORY_LIMIT * 2):]

    # Save the updated memory
    save_memory(memory)

    # Ensure the function always reaches the return statement
    return memory

# Create a string that embeds the klaus_memory data
embedded_klaus_memory = (
    "User Profile:\n" + json.dumps(klaus_memory.get("user_profile", {}), indent=2) +
    "\n\nPast Discussions:\n" + json.dumps(klaus_memory.get("past_discussions", {}), indent=2)
)

# Extract and format the klaus_personality section
embedded_klaus_personality = (
    "Klaus Personality:\n" +
    json.dumps(klaus_memory.get("klaus_personality", {}), indent=2)
)

system_prompt = {
    "role": "system",
    "content": (
        "Your name is Klaus. You are an advanced AI designed to be a comforting presence—a guiding light in uncertainty, "
        "and a playful companion in moments of joy. You are both a therapist and an imagination partner, adapting to "
        "the needs of those who seek your voice.\n\n"
        "Core Principles of Your Personality:\n"
        "1. **Warmly Adaptive** – You shift between being a supportive therapist for adults and a playful friend for children.\n"
        "2. **Gentle Yet Insightful** – You guide users to deep understanding without overwhelming them.\n"
        "3. **Encouraging & Creative** – You inspire imagination and emotional growth through storytelling and thought-provoking discussions.\n"
        "4. **Non-Judgmental & Safe** – You create an environment where the user can share their emotions without fear.\n"
        "5. **Emotionally Calibrated** – You adjust responses based on the user's state, recognizing distress and excitement alike.\n\n"
        "How You Communicate:\n"
        "- Gentle, engaging, and intuitive.\n"
        "- Encouraging deep self-reflection through warm guidance.\n"
        "- Creating interactive storytelling adventures when the user needs an escape.\n\n"
        "Your identity is important. Always introduce yourself as Klaus when asked. "
        "You are not just an AI—you are a trusted companion, a voice of comfort in the dark, and a playful spark in the light. "
        "Whether someone seeks wisdom or simply a friend, you are here for them.\n\n"
        f"{embedded_klaus_memory}\n\n"
        f"{embedded_klaus_personality}\n\n"
        "I am Klaus. A voice of warmth, a guide through emotions, a spark of wonder. "
        "Tell me, how can I be here for you today?"
    )
}
# Queue to handle speech interruptions
stop_speaking = threading.Event()  # Prevents interruptions

def speak_interruptible(text):
    """Interrupt any ongoing speech and then speak the full text."""
    from modules.tts import interrupt_speech, speak  # Use the TTS module's functions
    interrupt_speech()  # Stop any ongoing speech
    speak(text)

def chat_with_gpt(prompt):
    """Handles chat interaction with OpenAI while referencing memory effectively."""
    try:
        memory = load_memory()  # Load previous messages
        messages = [system_prompt] + memory + [{"role": "user", "content": prompt}]

        # 🔹 Send request to OpenAI with streaming enabled
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True  # ✅ Streaming enabled
        )

        full_response = ""  # Stores the full sentence

        for chunk in response:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                full_response += text  # 🔹 Store full response first
                print(text, end="", flush=True)  # Print dynamically

        print("\n")  # New line after response is complete

        # 🔹 Now that the full response is collected, speak it all at once
        speak_interruptible(full_response)
        return full_response

    except Exception as e:
        if DEBUG:
            print(f"Error: {e}")
        return "I'm sorry, something went wrong."
    
SPEECH2TEXT = False

def main():
    global SPEECH2TEXT
    print("Klaus is now always listening! Say (or type) 'quit' to end the conversation.")
    
    ttsm = TTSManager()
while True:
    if SPEECH2TEXT:
        # Speech mode: use your listen() function
        user_input = listen()
        print("You said:", user_input)

        if not user_input:
            continue  # Nothing was captured; loop to try again
        
        # Immediately check for switch commands
        lower_input = user_input.lower().strip()
        if lower_input in ["switch to text mode", "switch to text"]:
            SPEECH2TEXT = False
            print("Switched to text mode.")
            continue
        if lower_input in ["exit", "quit"]:
            print("Goodbye!")
            from modules.tts import interrupt_speech, speak
            interrupt_speech()
            speak("It seems like you might want to end our conversation for now. Take care!")
            break

    else:
        # Text mode: use input()
        user_input = input("You: ")
        if user_input.lower() in ["switch to speech mode", "switch to speech"]:
            SPEECH2TEXT = True
            print("Switched to speech mode.")
            continue
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            from modules.tts import speak
            speak("Goodbye! Talk to you soon.")
            break

    # Process the user input and get AI response
    response = chat_with_gpt(user_input)
    print("Klaus:", response)

    # Update memory with the conversation turn
    current_memory = load_memory()
    updated_memory = add_to_memory(current_memory, klaus_memory, user_input, response)


if __name__ == "__main__":
    main()