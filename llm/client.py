from openai import OpenAI
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import DEFAULT_MODEL, OLLAMA_MODEL, OLLAMA_BASE_URL, OPENAI_API_KEY
from llm.prompts import build_system_prompt

def ask_llm(context: str, messages: list[dict], provider: str = "OpenAI"):
    system_prompt = build_system_prompt(context)
    chat_messages =[{"role": "system", "content": system_prompt}] + messages
    if provider == "Ollama":
        client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key='ollama',
)
        response = client.chat.completions.create(
            messages = chat_messages,
            model=OLLAMA_MODEL,
)
        return response.choices[0].message.content

    else: 
        client = OpenAI(api_key= OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages = chat_messages
)

        return response.choices[0].message.content