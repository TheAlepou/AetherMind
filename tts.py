import pyttsx3
from langdetect import detect
import platform
# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

voices = tts_engine.getProperty('voices')

for voice in voices:
    print(f"ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")

def set_voice(language):
    voices = tts_engine.getProperty('voices')
    
    lang_map = {
        "en": "com.apple.speech.synthesis.voice.Alex",  # Example for English (MacOS)
        "ro": "com.apple.speech.synthesis.voice.Ioana",  # Example for Romanian (MacOS)
        "fr": "com.apple.speech.synthesis.voice.Thomas"  # Example for French
    }
    
    selected_voice = lang_map.get(language, None)
    
    if selected_voice:
        tts_engine.setProperty('voice', selected_voice)
    else:
        print(f"No dedicated voice found for '{language}', using default.")

def speak(text):
    """Speak the given text using pyttsx3."""
    system_name = platform.system()
    try:
        if system_name in ["Darwin", "Windows"]:
            tts_engine.stop()  # Stop any ongoing speech to prevent overlap
            tts_engine.setProperty('rate', 150)  # Set the desired rate
            language = detect(text)  # Auto-detect input language
            set_voice(language)  # Set the voice based on the detected language
            tts_engine.say(text)
            tts_engine.runAndWait()
        elif system_name == "Linux":
            print("Please install espeak if you're on Linux.")
            # Use espeak (ensure it's installed!)
            os.system(f'espeak "{text}"')
        else:
            print("Unsupported operating system.")
    
    except Exception as e:
        print(f"Error in speak(): {e}")