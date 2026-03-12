import streamlit as st
import tempfile
from main import ask_question, get_API_Key
import rag
import os

provider = st.selectbox("Model", ["OpenAI", "Ollama"])
file = st.file_uploader("File you want to use", "pdf")
question = st.chat_input("What is your question?")

def chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp: 
    tmp.write(file.read())
    tmp_path = tmp.name
if file != None and question != None:
    chat_history()
    collection_name = file.name
    get_API_Key()
    collection = rag.init_db(collection_name)
    rag.index_document(collection_name, collection)
    important_chunks = rag.query_collection(question, collection)
    with st.spinner("Wait for it..."):
        response = ask_question(
        "\n".join(important_chunks),
        question + "Give the answer in Markdown format",
        provider
)
        st.success("Done!")

    st.markdown(response)
    os.unlink(tmp_path)
