import sys
import os

# Add parent directory to path so python can find the app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from perfect_indian_app import app
