# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.rag_service import get_chain

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # lock down in prod
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ChatIn (BaseModel):
    session_id: str
    message: str

class ChatOut(BaseModel):
    answer: str
    sources: list[str]

_sessions: dict[str, list[tuple[str, str]]] = {}   # id -> [(role,msg), ...]

@app.post("/chat", response_model=ChatOut)
def chat(q: ChatIn):
    history = _sessions.setdefault(q.session_id, [])
    history.append(("user", q.message))
    chain   = get_chain()
    resp    = chain({"question": q.message, "chat_history": history})
    history.append(("assistant", resp["answer"]))
    return ChatOut(answer=resp["answer"],
                   sources=[s.metadata["source"] for s in resp["source_documents"]])
