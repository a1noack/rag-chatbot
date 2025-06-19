#!/usr/bin/env python3
from __future__ import annotations

import argparse, os, time
from datasets import load_dataset
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from tqdm.auto import tqdm
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=".env", override=True)   # looks for .env in CWD

# ---------- CLI ----------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("Build Chroma DB from rag-mini-wikipedia")
    p.add_argument("--persist_dir", default="storage")
    p.add_argument("--collection", default="wiki_mini")
    p.add_argument("--chunk_size", type=int, default=512)
    p.add_argument("--chunk_overlap", type=int, default=64)
    p.add_argument("--batch_size", type=int, default=128)
    p.add_argument("--max_docs", type=int, default=0, help="0 = all docs")
    return p.parse_args()

# ---------- Helpers ----------
def load_articles(max_docs: int | None = None):
    ds = load_dataset("rag-datasets/rag-mini-wikipedia", "text-corpus", split='passages')
    for i, item in enumerate(ds):
        if max_docs and i >= max_docs:
            break
        yield item['id'], item['passage']

# ---------- Main ----------
def main() -> None:
    t0 = time.time()
    args = parse_args()
    os.makedirs(args.persist_dir, exist_ok=True)
    print('Made local vector storage dir.')

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap
    )
    embedder = OpenAIEmbeddings(
        model="text-embedding-3-small",
        chunk_size=args.batch_size,
    )
    print('Instantiated text splitter and OpenAI embedding model objects.')

    # Re-use existing DB if present
    db_file = Path(args.persist_dir) / "chroma.sqlite3"
    if db_file.exists():
        db = Chroma(persist_directory=args.persist_dir,
                    collection_name=args.collection,
                    embedding_function=embedder)
        print(f"Vector store already has {db._collection.count()} chunks. Will not run embedding process again!")
        return

    print('Starting embedding process...')
    texts, metas = [], []
    for title, body in tqdm(list(load_articles(args.max_docs))):
        for chunk in splitter.split_text(body):
            texts.append(chunk)
            metas.append({"source": title})

    db = Chroma.from_texts(
        texts=texts,
        embedding=embedder,
        metadatas=metas,
        persist_directory=args.persist_dir,
        collection_name=args.collection,
    )
    db.persist()
    print(f"Done in {time.time() - t0:0.1f}s – {db._collection.count():,} chunks stored")

if __name__ == "__main__":
    main()
