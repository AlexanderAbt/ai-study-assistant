# AI Study Assistant

A small RAG (Retrieval-Augmented Generation) app for studying with your own documents. You upload one or more PDFs (lecture notes, scripts, papers), ask questions about them in a chat interface, and get answers that are based only on the content of those documents — including source references with file name and page number.

Answers can come from OpenAI (`gpt-4o-mini`) or from a local model via Ollama (`llama3.1:8b`), so you can also run it fully offline.

## How it works

1. Uploaded PDFs are read with PyMuPDF, page by page.
2. Each page is stored in a local ChromaDB collection (one collection per file), so documents only get indexed once.
3. When you ask a question, the 10 most relevant chunks are retrieved from the vector store.
4. Those chunks are passed as context to the LLM, which is instructed to answer only from the provided context. If the answer isn't in the documents, it says so instead of making something up.
5. The answer is shown in the chat together with the sources it was based on.

## Project structure

```
app/         Streamlit UI (chat, file upload, provider selection)
ingestion/   PDF loading and indexing into ChromaDB
retrieval/   Vector store setup and chunk retrieval
llm/         LLM client (OpenAI / Ollama) and system prompt
config/      Settings (models, API key, Ollama URL)
main.py      Simple CLI entry point
```

## Setup

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

If you want to use OpenAI, create a `.env` file in the project root:

```
OPENAI_API_KEY=your-key-here
```

If you want to use Ollama instead, make sure it's installed and running (`ollama serve`) and that you have pulled the model:

```bash
ollama pull llama3.1:8b
```

## Usage

Start the app with:

```bash
streamlit run app/streamlit_app.py
```

Then in the browser: pick a provider (OpenAI or Ollama), upload one or more PDFs, and ask your question in the chat input. The vector database is persisted locally in `chroma_db/`, and logs are written to `app.log`.

## Configuration

Models and the Ollama URL are defined in `config/settings.py`:

| Setting | Default |
| --- | --- |
| OpenAI model | `gpt-4o-mini` |
| Ollama model | `llama3.1:8b` |
| Ollama URL | `http://localhost:11434/v1/` |
