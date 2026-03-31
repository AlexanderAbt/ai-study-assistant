import fitz
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os

def read_file(file_path: str)-> tuple[list[str], list[int]]:
    text = ""
    chunks = []
    page_numbers = []
    try:
        with fitz.open(file_path) as doc:
            for page_num, page in enumerate(doc): 
                text = page.get_text()
                if text.strip(): 
                    chunks.append(text)
                    page_numbers.append(page_num + 1)
    except FileNotFoundError: 
        raise FileNotFoundError("The selected Document doesn't exist")
    if not chunks:
                raise ValueError("Could not extract text. Make sure it's not a scanned document.")
    return chunks, page_numbers
    