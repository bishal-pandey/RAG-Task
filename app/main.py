from fastapi import FastAPI
from api.ingestion import router as ingestion_router
from api.chat import router as chat_router

app = FastAPI()

app.include_router(ingestion_router, tags=["Document Ingestion"])
app.include_router(chat_router, tags=["Conversational RAG"])


@app.get("/")
def home():
    return {
        "message": "RAG Backend Running"
    }