import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from ingestion.pdf_loader import read_file
from chromadb import Collection
import logging
logger = logging.getLogger(__name__)
def index_document(filepath: str, collection: Collection, original_name: str) -> None:
    if collection.count() > 0:
        logger.info(f"Document {original_name} already indexed, skipping")
        return
    logger.info(f"Indexing document: {original_name}")
    chunks, page_numbers = read_file(filepath)
    logger.info(f"Extracted {len(chunks)} pages from {original_name}")
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        ids = ids,
        documents = chunks,
        metadatas = [{"page": page_num, "source": original_name} for page_num in page_numbers]
    )
    logger.info(f"Successfully indexed {original_name} chunks")