from dotenv import load_dotenv
import os
import fitz
import openai
from openai import OpenAI

def get_API_Key():
    load_dotenv()
    key = os.environ.get('OPENAI_API_KEY')
    if key is None:
       raise ImportError("OpenAI_KEY wasn't found")
    else: 
        return key

def read_file(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc: 
            text += page.get_text()
    return text

def ask_question(text, question):
    client = OpenAI()
    response = client.responses.create(
    model="gpt-4o-mini",
    input= text + question 
)
    return response

    
if __name__ == "__main__":
    get_API_Key()
    output = ask_question(
        read_file("test_document.pdf"),
        "Summarize the content of the following document"
)
    print(output)