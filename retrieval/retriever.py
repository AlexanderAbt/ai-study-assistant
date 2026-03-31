from chromadb import Collection 
import logging

logger = logging.getLogger(__name__)

def retrieve_chunks(question: str, collection: Collection)-> tuple[list[str], list[dict]]:
    logger.info(f"Retrieving chunks for question: {question[:50]} from database...")
    result = collection.query(
        query_texts = [question],
        n_results = 10,
        include =["documents", "metadatas"]
    )
    return result["documents"][0], result["metadatas"][0]