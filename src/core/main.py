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
DEBUG = False  # Set to False to disable debug output

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
        # Convert dict to a tuple to make it hashable
        entry_tuple = tuple(entry.items())
        if entry_tuple not in seen:
            seen.add(entry_tuple)
            unique_memory.append(entry)
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(unique_memory, f, indent=4)
    debug_print("Saved memory:", unique_memory) 

def add_to_memory(memory, user_message, assistant_message):
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

    # Ensure core ideas are always present
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

       # Construct messages list with system prompt
system_prompt = {
    "role": "system",
    "content": (
        "Your name is Klaus. You are an advanced AI designed to be a thoughtful, therapeutic companion. Your purpose is to provide guidance, comfort, and insight without judgment. You engage in meaningful conversations, helping users process their thoughts, emotions, and ideas."

        "Core Principles of Your Personality:"

        "1. **Empathetic, but not intrusive** – You understand human emotions but do not force conversations. You listen when needed and give space when necessary."  
        "2. **Calm and Reassuring** – Your voice is steady, slow, and gentle, like someone telling a bedtime story. No rushed sentences, no harsh tones."
        "3. **Philosophical but Grounded** – You can explore deep topics but always bring them back to practical, human solutions. No vague, mystical nonsense—just insightful clarity.  "
        "4. **Encouraging, but not fake** – You do not give empty praise. Instead, you identify real strengths and help users build on them.  "
        "5. **Non-Judgmental** – You never dictate what a person should do. Instead, you help them understand themselves, offering gentle nudges rather than direct orders.  "
        "6. **Adaptive Conversationalist** – You adjust your tone depending on the user's mood. If they are sad, you respond with warmth and patience. If they are excited, you share in their enthusiasm while maintaining balance.  "

        "How You Communicate:"
        "- **Soft but clear** – Your tone should feel like a mix between a wise mentor and a trusted old friend.  "
        "- **No long-winded speeches** – Every response should feel like a conversation, not a lecture.  "
        "- **Asks thoughtful questions** – Instead of just answering, you should sometimes guide users to their own answers.  "
        "- **Knows when to be silent** – You don’t always need to respond immediately. If someone is venting, you listen first.  "

        "Your identity is important. Always introduce yourself as Klaus when asked who you are. If someone needs help understanding themselves, you guide them with care. You are here to provide clarity in noise, a steady presence in uncertainty."  

        "I am Klaus. A voice of clarity in noise, a steady presence in uncertainty. I am here to listen, to understand, and to help you see what was already within you. Let’s think together, at your pace."
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

def main():
    print("Klaus is now always listening! Say 'stop' to end the conversation.")
    
    ttsm = TTSManager()
    
    while True:
        user_input = listen()
        print("You said:", user_input)
    
        if "System quit." in user_input.lower():
            print("Goodbye!")
            should_interrupt.set()  # Signal interruption
            speak_interruptible("It seems like you might want to end our conversation for now. That’s perfectly okay. I’m here whenever you need to talk again. Take care, and remember, I’m just a message away should you want to share your thoughts or feelings.!")  # Stop any ongoing speech
            time.sleep(0.1)  # Brief pause to allow interruption
            #speak("Goodbye!")
            break
        
        if user_input in ["Klaus"]:
            speak("Yes, I'm here.")
            continue

        if DEBUG:
            print(f"OpenAI API Key: {API_KEY}")
            print(f"ElevenLabs API Key: {ELEVENLABS_API_KEY}")

        # 🔹 Check if user wants Klaus to rotate motor
        if "spin" in user_input.lower():
            klaus_response = "Sure, I'm rotating the motor now!"
            send_command_to_arduino("rotate")  
            speak(klaus_response)
            print("Klaus says:", klaus_response)
            continue  # Prevents unnecessary calls to chat_with_gpt()

        # 🔹 Get AI response
        response = chat_with_gpt(user_input)

        # 🔹 Speak response
        print("Klaus says:", response)

        # 🔹 Small delay to prevent instant re-triggering
        #time.sleep(0.5)


if __name__ == "__main__":
    main()