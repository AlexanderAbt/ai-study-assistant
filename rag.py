from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from utils import read_file


def init_db():
    client = chromadb.Client()
    return client.create_collection(name="chunks_collection")

def index_document(file_path, collection):
    text = read_file(file_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    chunks = text_splitter.split_text(text)
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        ids = ids,
        documents = chunks
    )

def query_collection(question, collection):
    result = collection.query(
        query_texts = [question],
        n_results = 5 
    )
    return result["documents"][0]