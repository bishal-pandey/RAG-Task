from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Document
from dotenv import load_dotenv
import os
load_dotenv()

QDRANT_API = os.getenv("QDRANT_API")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
QDRANT_HOST = os.getenv("QDRANT_HOST")

class QdrantVectorDB:
    def __init__(self):
        try:
            self.collection_name = QDRANT_COLLECTION
            self.client = QdrantClient(url="https://6b6aaed2-4c1d-4069-80c3-bbdbfad503b7.us-east-1-1.aws.cloud.qdrant.io",
                                        port=6333,
                                        api_key = QDRANT_API
                                        )
                 
        except Exception as e:
            print(f"Error initializing Qdrant client: {e}")
            self.client = None
        if not self.client.collection_exists(self.collection_name):               
            self._create_collection()
        
    def _create_collection(self):
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config = VectorParams(size=384, distance=Distance.COSINE)
        )
    def insert_vector(self, vector_id, vectors, payload):
        points = PointStruct(id=vector_id, vector=vectors, payload=payload)

        self.client.upsert(
            collection_name=self.collection_name,
            points=[points],
            
        )
