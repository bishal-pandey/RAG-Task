# Conversational RAG Backend

A production-style Retrieval-Augmented Generation (RAG) backend built with **FastAPI**. The project provides document ingestion, semantic search, multi-turn conversations using Redis, and AI-powered interview booking.

## Features

* Upload **PDF** and **TXT** documents
* Extract and preprocess document text
* Support multiple chunking strategies
* Generate embeddings for document chunks
* Store embeddings in **Qdrant**
* Store document metadata in **SQLite**
* Custom RAG pipeline (no `RetrievalQAChain`)
* Multi-turn conversations using **Redis** chat memory
* Context-aware question answering
* AI-powered interview booking
* Store interview booking details in a database
* REST APIs built with **FastAPI**

---

## Tech Stack

* FastAPI
* Python
* Qdrant
* Redis
* SQLite
* SQLAlchemy
* Google Gemini
* PyPDF
* Sentence Embeddings

---

## Project Structure

```text
Rag-Task
├── app/
│   ├── main.py
│ 
├── api
│  ├── ingestion.py
│  ├── chat.py
│
├── services/
│   ├── ingestionService.py
│   ├── combineService.py
│   ├── embedding.py
│   ├── LLM.pt
│   ├─ retriever.py
│   └── redis.py
│
├── db/
│   ├── booking_db.py
│   ├─ sql_db.py
│   └── vector_db.py
│
├── .env
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/<repository>.git
cd <repository>
```


Activate it:

### Windows

```bash
venv\Scripts\activate
```


Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_api_key

QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=documents

REDIS_HOST=localhost
REDIS_PORT=6379


EMBEDDING_MODEL=models/text-embedding-004
LLM_MODEL=gemini-2.5-flash
```

---

## Running the Application

```bash
uvicorn main:app --reload
```

Open the interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Document Ingestion

**POST** `/ingest`
strategy : TokenBased/ChunkBased
Uploads a PDF or TXT document, extracts text, chunks the content, generates embeddings, stores vectors in Qdrant, and saves metadata.

---

### Conversational RAG

**POST** `/chat`

Accepts a user question and session ID, retrieves relevant document chunks, combines them with chat history from Redis, and generates a context-aware response.
  {session_id:session_id,
  quesion:Prompt_to_llm"}
  
---

## Workflow

1. Upload a PDF or TXT document.
2. Extract document text.
3. Split text into chunks.
4. Generate embeddings.
5. Store embeddings in Qdrant.
6. Save metadata in SQLite.
7. Receive user questions.
8. Retrieve relevant document chunks.
9. Load conversation history from Redis.
10. Generate responses using the LLM.
11. Save updated conversation history.
12. Detect interview booking requests and store booking details.

---

