import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

os.environ["GEMINI_API_KEY"] = "dummy_key"
os.environ["DATABASE_URL"] = "sqlite:///test.db"
