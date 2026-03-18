import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4o-mini"
OLLAMA_MODEL = "llama3.2"
OLLAMA_BASE_URL = "http://localhost:11434/v1/"