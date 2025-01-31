import requests
import os
import pygame  # To play the generated audio
from dotenv import load_dotenv

# Load API key from environment variable
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "iP95p4xoKVk53GoZ742B"  # Replace with the correct voice ID

# Load API key from .env file
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ElevenLabs API URL
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Voice ID for 'Chris - Conversational' (Check your ElevenLabs dashboard for exact ID)
CHRIS_VOICE_ID = "iP95p4xoKVk53GoZ742B"  # Replace this with the actual voice ID

def speak(text):
    """Convert text to speech using ElevenLabs API and play the audio."""
    try:
        # API request to generate speech
        response = requests.post(
            f"{ELEVENLABS_URL}/{CHRIS_VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"},
            json={"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}}
        )

        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.3,  # Less robotic, more expressive
                "similarity_boost": 0.7,  # More natural, less "perfect"
                "style": 0.6,  # More storytelling vibe
                "use_speaker_boost": True
            }
        }
        # Check for errors
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return

        # Save audio file
        audio_file = "output.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)

        # Play the audio using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait until audio is done playing
        while pygame.mixer.music.get_busy():
            continue

    except Exception as e:
        print(f"Error in speak(): {e}")