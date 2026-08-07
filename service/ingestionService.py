from service.embedding import Embedding
from db.vector_db import QdrantVectorDB
from service.chunking import Chunker
from db.sql_db import Database, DocumentMetaData
import datetime
import uuid

class IngestionService:
    def __init__(self, chunk_size=100, overlap=10):
        self.chunker = Chunker(chunk_size, overlap)
        self.embedding_model = Embedding()
        self.vector_db = QdrantVectorDB()
        self.db = Database()

    def process_document(self, filename, document_id, document, strategy):
        chunks = self.chunker.chunking_method(document, strategy)
        embeddings = self.embedding_model.transform(chunks)
        print(f"Generated embeddings for {len(embeddings)} chunks.")
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = str(uuid.uuid4())
            # vectors_id.append(vector_id)

            payload={
                'filename':filename,
                'chunk_index': idx, 
                "chunk_text": chunk,
            }
            # payloads.append(payload)
            self.vector_db.insert_vector(
                vector_id = vector_id,
                vectors = embedding,
                payload = payload
            )
            print("Inserted chunk vector into Qdrant")
        document_metadata = DocumentMetaData(
            document_id=document_id,
            filename=filename,
            chunking_strategy="token_based",
            chunk_size=self.chunker.chunk_size,
            total_chunks=len(chunks),
            created_at=datetime.datetime.now()
        )
        db_session = self.db.get_session()
        try:
            db_session.add(document_metadata)
            db_session.commit()
            print(f"Document metadata for '{filename}' saved to the database.")
        except Exception as e:
            print(f"Error saving document metadata: {e}")
        finally:
            db_session.close()
        
ingest = IngestionService()