import requests
import os
import time
import pygame
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
VOICE_ID = "iP95p4xoKVk53GoZ742B"

# Voice settings for natural conversation
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.7
}

def speak(text):
    """Convert text to speech and play it"""
    if not text:
        return
        
    try:
        # Generate speech from text
        response = requests.post(
            f"{ELEVENLABS_URL}/{VOICE_ID}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "voice_settings": VOICE_SETTINGS
            }
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return

        # Save and play audio
        audio_file = "response.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for audio to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Cleanup
        pygame.mixer.quit()
        os.remove(audio_file)

    except KeyboardInterrupt:
        print("\nSpeech interrupted")
        pygame.mixer.quit()
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")
    
    except Exception as e:
        print(f"Error in text-to-speech: {e}")