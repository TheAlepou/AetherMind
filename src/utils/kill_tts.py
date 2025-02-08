import os
import sys
import time
import signal
import subprocess
from pathlib import Path

class TTSManager:
    def __init__(self):
        self.process = None
        self.tts_path = Path(__file__).parent.parent / "modules" / "tts.py"
        
    def start(self):
        """Start TTS process"""
        if self.process and self.process.poll() is None:
            print("TTS already running")
            return
            
        self.process = subprocess.Popen(['python', str(self.tts_path)])
        print("TTS started")
        
    def kill(self):
        """Kill TTS process"""
        if self.process and self.process.poll() is None:
            self.process.kill()
            print("TTS killed")
        else:
            print("No TTS process running")

def main():
    ttsm = TTSManager()
    
    # Handle Ctrl+C
    def signal_handler(sig, frame):
        print("\nShutting down TTS...")
        ttsm.kill()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()