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

import threading
from queue import Queue

# Add global state tracking
is_speaking = threading.Event()
should_interrupt = threading.Event()
audio_queue = Queue()

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "audio")
RESPONSE_FILE = os.path.join(AUDIO_DIR, "response.mp3")

def ensure_audio_dir():
    """Create audio directory if it doesn't exist"""
    os.makedirs(AUDIO_DIR, exist_ok=True)

def speak(text):
    """Convert text to speech and play it with interrupt support"""
    if not text:
        return
        
    try:
        ensure_audio_dir()
        is_speaking.set()
        should_interrupt.clear()
        
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

        # Save audio to file
        with open(RESPONSE_FILE, "wb") as f:
            f.write(response.content)

        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(RESPONSE_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() and not should_interrupt.is_set():
            pygame.time.wait(100)

    finally:
        is_speaking.clear()
        pygame.mixer.quit()
        if os.path.exists(RESPONSE_FILE):
            os.remove(RESPONSE_FILE)


def interrupt_speech():
    """Call this from speech input when voice is detected"""
    if is_speaking.is_set():
        should_interrupt.set()