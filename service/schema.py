from pydantic import BaseModel, Field
from datetime import datetime

class MetaDaataSchema(BaseModel):
    document_id: int 
    filename:str
    chunking_strategy: str
    chunk_size:int
    total_chunks:int
    created_at:datetime