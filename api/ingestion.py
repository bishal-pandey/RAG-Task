import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from ingestionService import IngestionService

router = APIRouter()

ingestion_service = IngestionService(chunk_size=100, overlap=10)
router.post("/ingest")
async def ingest_document(strategy:str,file: UploadFile = File()):

    if file.filename.endswith(".pdf"):
        document = ""
        reader = PdfReader(file.file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                document +=text + "\n"
    elif file.filename.endswith(".txt"):
        document = await(file.read()).decode("utf-8")

    else:
        raise HTTPException(status_code=400, detail="This file type is not supported. Upload either PDF or txt")

    document_id = str(uuid.uuid4())
    embedding = ingestion_service.process_document(file.filename, document_id, document, strategy)
    return {
        "document_id": document_id,
        "filename": file.filename,
        "status": "Document ingested and processed successfully.",
            }
