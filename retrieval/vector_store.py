import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
import chromadb
import logging
import re
import unicodedata

logger = logging.getLogger(__name__)

def santize_name(name : str) -> str: 
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    name = name.strip("._-")
    return name

def get_collection(file_path: str) -> chromadb.Collection:
    collection_name = santize_name(file_path)
    logger.info(f"Creating or getting collection for {file_path}")
    client = chromadb.PersistentClient(path = "chroma_db/")
    return client.get_or_create_collection(collection_name)