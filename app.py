import streamlit as st
import tempfile
from main import ask_question, get_API_Key
import rag
import os

provider = st.selectbox("Model", ["OpenAI", "Ollama"])
file = st.file_uploader("File you want to use", "pdf")
question = st.chat_input("What is your question?")

def get_important_chunks(file, question): 
    collection_name = file.name
    get_API_Key()
    collection = rag.init_db(collection_name)
    rag.index_document(collection_name, collection)
    return rag.query_collection(question, collection)

if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question is not None:
    if file is not None:
        with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp: 
            tmp.write(file.read())
            tmp_path = tmp.name
        important_chunks = get_important_chunks(file, question)

    if file is None:
        important_chunks = []

    st.session_state.messages.append({"role": "user", "content": question})
    get_API_Key()
    with st.spinner("Wait for it..."):
        response = ask_question(
        "\n".join(important_chunks),
        st.session_state.messages,
        provider
)
    st.success("Done!")
    st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    print("Messages:", st.session_state.messages)
    if file is not None: 
        os.unlink(tmp_path)