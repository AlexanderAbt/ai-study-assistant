from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from utils import read_file


def init_db(file_path):
    client = chromadb.PersistentClient(path = "chroma_db/")
    return client.get_or_create_collection(name=file_path)

def index_document(file_path, collection):
    if collection.count() > 0:
        return
    text = read_file(file_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        ids = ids,
        documents = chunks
    )

def query_collection(question, collection):
    result = collection.query(
        query_texts = [question],
        n_results = 10
    )
    return result["documents"][0]