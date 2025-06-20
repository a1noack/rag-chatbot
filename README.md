# Wikipedia RAG Chatbot

A Retrieval-Augmented Generation (RAG) demo using Wikipedia as the knowledge base. The backend is powered by FastAPI, LangChain, and ChromaDB, and the frontend is built with Vue.js and Vite.

## Prerequisites

- Docker (v20+) & Docker Compose (v2+)
- A valid OpenAI API key stored in a `.env` file at the project root:
  ```bash
  OPENAI_API_KEY=sk-...YOUR_KEY_HERE...
  ```

## Services Overview

- **api**: FastAPI server (port `8000`)
- **web**: Vue.js development server (port `5173`)
- **ingest**: One-off ingestion container that generates vector embeddings and populates `storage/`

## Quick Start (Containerized)

1. Build and run the ingestion job to chunk and vectorize the "rag-mini-wikipedia" dataset:
   ```bash
   docker compose run --rm ingest -- \
             --persist_dir /app/storage \
             --chunk_size 500 \
             --model text-embedding-ada-002
   ```
   Note that you can pass several parameters to the ingestion job to control the vectorization process. For a full list of parameters to pass, check `scripts/ingest.py` lines 18-24.
   
   This will create or update the `storage/` folder with the ChromaDB vector store.

2. Launch the API and Web services:
   ```bash
   docker compose up --build
   ```

3. Open your browser and visit:
   - Frontend:  http://localhost:5173
   - Backend API OpenAPI docs:  http://localhost:8000/docs

4. Ask questions in the web UI, powered by your local RAG backend.

## Teardown & Reset

- To stop all running containers:
  ```bash
  docker compose down
  ```
- To remove the vector store and start fresh:
  ```bash
  docker compose down --volumes
  rm -rf storage/
  ```

## Local Development (Optional)

If you prefer not to use Docker, you can run everything locally in a Python virtual environment:

1. Create & activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Generate embeddings:
   ```bash
   python scripts/ingest.py --persist_dir storage
   ```

3. Start the backend with live reload:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. In another shell, start the frontend:
   ```bash
   cd frontend
   npm ci
   npm run dev -- --host 0.0.0.0
   ```

5. Visit http://localhost:5173 and enjoy!

## Repository Layout

- `app/` — FastAPI application code
- `frontend/` — Vue.js client application
- `scripts/ingest.py` — data ingestion & embedding script
- `storage/` — local vector store (ChromaDB files)
- `Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml` — container definitions

---
