# rag-chatbot

# Setup
1. Create a Python virtual environment with Python 3.10+ `python -m venv .venv`.
2. Activate the virtual environment `source .venv/bin/activate` and install the requirements `pip install -r requirements.txt`.
3. Ensure you have a `.env` file at the root of this directory with your OpenAI API key.
4. Run the ingestion script to generate vector embeddings of the wikipedia dataset.
5. Build the vector store. `python ingest.py --persist_dir storage`. A `storage/` folder will appear containing chroma.sqlite and you'll be ready for the FastAPI RAG backend.