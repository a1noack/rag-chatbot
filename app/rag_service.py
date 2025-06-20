# app/rag_service.py
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path=".env", override=True)   # looks for .env in CWD

print(os.getenv('OPENAI_API_KEY'))

PERSIST_DIR = "storage"
COLLECTION  = "wiki_mini"

@lru_cache(1)  # load once per process
def get_chain() -> ConversationalRetrievalChain:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv('OPENAI_API_KEY'))
    vectordb   = Chroma(
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION,
        embedding_function=embeddings,
    )
    llm   = ChatOpenAI(model_name="gpt-4o-mini", api_key=os.getenv('OPENAI_API_KEY'))        # adjust if needed
    chain = ConversationalRetrievalChain.from_llm(
        llm, vectordb.as_retriever(search_kwargs={"k": 4}), return_source_documents=True
    )
    return chain
