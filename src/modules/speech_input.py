import openai
import pyaudio
import queue
import os
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import webrtcvad  # ✅ Voice Activity Detection
import noisereduce as nr  # ✅ Noise Reduction
import time
import wave
import io
import signal
import sys
import tempfile
import threading
from filelock import FileLock
from queue import Queue, Empty
from .tts import interrupt_speech


# Add these constants at the top with other constants
DEBUG = False  # Toggle debug prints
PRINT_COOLDOWN = 0.5  # Minimum seconds between voice detection prints

# Load API Key
API_KEY = os.getenv("OPENAI_API_KEY")

# Update constants
SAMPLE_RATE = 16000
CHUNK_SIZE = 480  # Reduced for faster processing
MAX_RECORD_TIME = 30
SILENCE_TIME = 3.0 # 3 seconds of silence
SILENCE_THRESHOLD = 0.01
CONSECUTIVE_SILENCE_FRAMES = 3  # New constant

# Initialize VAD
vad = webrtcvad.Vad(3)  # Aggressive mode

def transcribe_audio(audio_file):
    """Transcribe audio using Whisper API"""
    try:
        with open(audio_file, "rb") as f:
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return response.text
    except Exception as e:
        print(f"⚠️ Transcription error: {e}")
        return ""
    finally:
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except:
            pass

def save_audio(audio_data):
    """Save audio data to WAV file"""
    # Create audio directory if it doesn't exist
    audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    # Generate unique filename
    audio_file = os.path.join(audio_dir, f"speech.wav")

    try:
        with wave.open(audio_file, "wb") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_data)
        return audio_file
    except Exception as e:
        print(f"⚠️ Error saving audio: {e}")
        return None


def listen():
    q = Queue()
    last_audio_time = time.time()
    audio_data = b""
    silence_counter = 0
    recording = True

    def callback(indata, frames, cb_time, status):
        nonlocal last_audio_time, silence_counter
        if status:
            print(status, flush=True)
            
        # Convert input to float32 and remove NaN/Inf
        np_data = np.nan_to_num(
            np.frombuffer(indata, dtype=np.int16).astype(np.float32) / 32768.0,
            nan=0.0, posinf=1.0, neginf=-1.0
        )
        
        # Calculate intensity from clean data
        audio_intensity = np.abs(np_data).mean()
        
        # Convert back to int16 for VAD
        vad_data = np.clip(np_data * 32767, -32768, 32767).astype(np.int16)
        
        try:
            # Ensure frame duration matches VAD requirements (10, 20, or 30ms)
            is_speech = vad.is_speech(vad_data.tobytes(), SAMPLE_RATE)
        except Exception as e:
            is_speech = False
        
        if audio_intensity > SILENCE_THRESHOLD or is_speech:
            interrupt_speech()
            q.put(vad_data.tobytes())
            last_audio_time = time.time()
            silence_counter = 0
        else:
            silence_counter += 1
            if silence_counter >= CONSECUTIVE_SILENCE_FRAMES:
                q.put(None)

    try:
        stream = sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=CHUNK_SIZE,
            dtype="int16",
            channels=1,
            callback=callback
        )
        
        with stream:
            start_time = time.time()
            print("🎤 Speak now...")
            
            while recording:
                try:
                    new_audio = q.get(timeout=0.5)
                    if new_audio is None:
                        if time.time() - last_audio_time > SILENCE_TIME:
                            print("🛑 Silence detected.")
                            break
                        continue
                    
                    audio_data += new_audio

                    if time.time() - start_time > MAX_RECORD_TIME:
                        print("🛑 Max time reached.")
                        break

                except Empty:
                    continue

                except KeyboardInterrupt:
                    print("\n🛑 Recording stopped by user")
                    recording = False
                    return ""

    finally:
        recording = False
        if stream is not None:
            stream.stop()
            stream.close()

    if len(audio_data) > 0:
        audio_file = save_audio(audio_data)
        if audio_file:
            transcribed_text = transcribe_audio(audio_file)
            if transcribed_text:
                return transcribed_text
    
    print("⚠️ No transcription available")
    return ""