from chromadb import Collection 
def retrieve_chunks(question: str, collection: Collection)-> tuple[list[str], list[dict]]:
    result = collection.query(
        query_texts = [question],
        n_results = 10,
        include =["documents", "metadatas"]
    )
    return result["documents"][0], result["metadatas"][0]