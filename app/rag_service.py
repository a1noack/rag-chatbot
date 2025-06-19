# app/rag_service.py
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

PERSIST_DIR = "storage"
COLLECTION  = "wiki_mini"

@lru_cache(1)  # load once per process
def get_chain() -> ConversationalRetrievalChain:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb   = Chroma(
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION,
        embedding_function=embeddings,
    )
    llm   = ChatOpenAI(model_name="gpt-4o-mini")        # adjust if needed
    chain = ConversationalRetrievalChain.from_llm(
        llm, vectordb.as_retriever(search_kwargs={"k": 4})
    )
    return chain
