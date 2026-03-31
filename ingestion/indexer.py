import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from ingestion.pdf_loader import read_file
from chromadb import Collection

def index_document(filepath: str, collection: Collection, original_name: str) -> None:
    if collection.count() > 0:
        return
    chunks, page_numbers = read_file(filepath)
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        ids = ids,
        documents = chunks,
        metadatas = [{"page": page_num, "source": original_name} for page_num in page_numbers]
    )