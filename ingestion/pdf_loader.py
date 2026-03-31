import fitz
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os
import logging

logger = logging.getLogger(__name__)

def read_file(file_path: str)-> tuple[list[str], list[int]]:
    text = ""
    chunks = []
    page_numbers = []
    try:
        logger.info(f"Reading File: {file_path}")
        with fitz.open(file_path) as doc:
            for page_num, page in enumerate(doc): 
                text = page.get_text()
                if text.strip(): 
                    chunks.append(text)
                    page_numbers.append(page_num + 1)
            logger.info(f"Read file {file_path} and retrieved {len(chunks)} pages")
    except FileNotFoundError: 
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError("The selected Document doesn't exist")
    if not chunks:
                logger.warning(f"No text extracted from {file_path}")
                raise ValueError("Could not extract text. Make sure it's not a scanned document.")
    logger.info("Returning chunks and page numbers")
    return chunks, page_numbers
    