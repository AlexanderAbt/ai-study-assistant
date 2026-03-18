from dotenv import load_dotenv
import os
import fitz
from openai import OpenAI
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from ingestion import indexer
from retrieval import vector_store
from retrieval import retriever
from llm import client


if __name__ == "__main__":
    
    provider_choice = input("Please select provider (OpenAI or Ollama)")
    question = input("What is your question regarding this document?")
    collection = vector_store.get_collection("skript.pdf")
    indexer.index_document("skript.pdf", collection)
    important_chunks = retriever.retrieve_chunks(question, collection, provider_choice)
    response = client.ask_llm(
        context = "\n".join(important_chunks), 
        messages = [{"role": "user", "content" : question}],
        provider = provider_choice
    )
    print(response)
    
    