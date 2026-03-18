import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
import tempfile
import os
from retrieval.vector_store import get_collection
from ingestion.indexer import index_document
from retrieval.retriever import retrieve_chunks
from llm.client import ask_llm


def safe_uploaded_file(file):
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp: 
        tmp.write(file.read())
        return tmp.name

st.title("RAG Learning Assistant")

provider = st.selectbox("Model", ["OpenAI", "Ollama"])
files = st.file_uploader("Upload PDF files", type= "pdf", accept_multiple_files = True)
question = st.chat_input("What is your question?")

if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question:
    important_chunks = []
    temp_paths = []
    if files:
        for file in files:
            tmp_path = safe_uploaded_file(file)
            temp_paths.append(tmp_path)
            collection = get_collection(file.name)
            index_document(tmp_path, collection)
            important_chunks.extend(retrieve_chunks(question, collection))

    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner("Wait for it..."):
        response = ask_llm(
        "\n".join(important_chunks),
        st.session_state.messages,
        provider
)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    print("Messages:", st.session_state.messages)

    for tmp_path in temp_paths:
        os.unlink(tmp_path)