# run.py
import os
import sys

# Add the `src` directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import and run the main file
from src.core.main import main

if __name__ == "__main__":
    main()