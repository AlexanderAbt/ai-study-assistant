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


def safe_uploaded_file(file: UploadedFile)-> str:
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
    all_metadatas = []
    if not files: 
        st.warning("Please upload a file")
        st.stop()
    if files:
        for file in files:
            try: 
                tmp_path = safe_uploaded_file(file)
                temp_paths.append(tmp_path)
                collection = get_collection(file.name)
                index_document(tmp_path, collection, file.name)
                chunks, metadatas = retrieve_chunks(question, collection)
                important_chunks.extend(chunks)
                all_metadatas.extend(metadatas)
            except ValueError as e:
                st.error(str(e)) 
            except FileNotFoundError as e:
                st.error(str(e)) 
            except Exception as e: 
                st.error(f"Unexpected error ocurred: {e}")

    st.session_state.messages.append({"role": "user", "content": question})

    try:
        with st.spinner("Wait for it..."):
            response = ask_llm(
            "\n".join(important_chunks),
            st.session_state.messages,
            provider
)
    except ValueError as e: 
        st.error(str(e))
        st.stop()
    except ConnectionError as e: 
        st.error(str(e))
        st.stop()
    except Exception as e: 
        st.error(f"Unexpected error occured: {e}")
        st.stop()
    with st.chat_message("assistant"):
        st.markdown(response)
        if all_metadatas: 
            sources = []
            for i, m in enumerate(all_metadatas):
                source_line = "[" + str(i+1) + "] " + m['source'] + ", Page " + str(m['page'])
                sources.append(source_line)
            source_answer = "**Sources:**\n\n" + "\n""\n".join(sources)
            response = response + "\n" + source_answer
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    print("Messages:", st.session_state.messages)

    for tmp_path in temp_paths:
        os.unlink(tmp_path)