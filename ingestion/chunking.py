import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from ingestion.pdf_loader import read_file
import os

def split_text(file_path : str, collection : chromadb.Collection) -> str:
    if collection.count() > 0:
        return
    text = read_file(os.path.basename(file_path))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    return text_splitter.split_text(text)
