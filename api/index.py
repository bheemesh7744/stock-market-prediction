import sys
import os

# Add the parent directory to the path so python can find perfect_indian_app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from perfect_indian_app import app
