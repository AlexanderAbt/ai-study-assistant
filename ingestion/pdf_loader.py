import fitz
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os

def read_file(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc: 
            text += page.get_text()
    return text