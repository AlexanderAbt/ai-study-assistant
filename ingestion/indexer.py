import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from ingestion.pdf_loader import read_file
from ingestion.chunking import split_text

def index_document(filepath, collection):
    if collection.count() > 0:
        return
    text = read_file(filepath)
    chunks = split_text(text, collection)
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        ids = ids,
        documents = chunks
    )