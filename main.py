from dotenv import load_dotenv
import os
import fitz
from openai import OpenAI
from utils import read_file

def get_API_Key():
    load_dotenv()
    key = os.environ.get('OPENAI_API_KEY')
    if key is None:
       raise ImportError("OpenAI_KEY wasn't found")
    else: 
        return key

def parse_output(response):
    answer = response.output[0].content[0].text
    return answer

def ask_question(text, question, provider = "OpenAI"):
    if provider == "Ollama":
        client = OpenAI(
        base_url='http://localhost:11434/v1/',
        api_key='ollama',
)
        response = client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': text + question,
                }
            ],
        model='llama3.2',
)
        return response.choices[0].message.content

    else: 
        client = OpenAI()
        response = client.responses.create(
            model="gpt-4o-mini",
            input= text + question 
)

        return parse_output(response)

if __name__ == "__main__":
    get_API_Key()
    provider_choice = input("Please select provider (OpenAI or Ollama)")
    response = ask_question(
        read_file("test_document.pdf"),
        "Summarize the content of the following document",
        provider_choice
)
    print(response)
    