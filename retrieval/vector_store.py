import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
import chromadb
import logging

logger = logging.getLogger(__name__)


def get_collection(file_path: str) -> chromadb.Collection:
    logger.info(f"Creating or getting collection for {file_path}")
    client = chromadb.PersistentClient(path = "chroma_db/")
    return client.get_or_create_collection(file_path)