def retrieve_chunks(question, collection):
    result = collection.query(
        query_texts = [question],
        n_results = 10
    )
    return result["documents"][0]