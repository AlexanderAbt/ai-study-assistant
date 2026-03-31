from openai import OpenAI
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import DEFAULT_MODEL, OLLAMA_MODEL, OLLAMA_BASE_URL, OPENAI_API_KEY
from llm.prompts import build_system_prompt
import openai
import logging

logger = logging.getLogger(__name__)
def ask_llm(context: str, messages: list[dict], provider: str = "OpenAI") -> str:
    logger.info("Build system prompt")
    system_prompt = build_system_prompt(context)
    chat_messages =[{"role": "system", "content": system_prompt}] + messages
    if provider == "Ollama":
        
        client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key='ollama',
)
        try: 
            logger.info("Ask Ollama for response")
            response = client.chat.completions.create(
                messages = chat_messages,
                model=OLLAMA_MODEL,
)
        except openai.APIConnectionError:
            logger.error("Connection to Ollama failed, writing Error message")
            raise ConnectionError("Couldn't connect to Ollama. Is it running? Use 'ollama serve' ") 

        return response.choices[0].message.content

    else: 
        if not OPENAI_API_KEY:
            raise ValueError("API key is missing")
        try:
            logger.info("Establishing connection to OpenAI")
            client = OpenAI(api_key= OPENAI_API_KEY)
            logger.info("Ask OpenAI for response")
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages = chat_messages
)
        except openai.AuthenticationError:
            raise ValueError("Invalid API key")
        except openai.APIConnectionError:
            raise ConnectionError("Could not connect to OpenAI")
        return response.choices[0].message.content