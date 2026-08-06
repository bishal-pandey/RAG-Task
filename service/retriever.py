# from qdrant_client import QdrantClient
# from qdrant_client.models import SearchRequest
class Retrieval:
    def __init__(self, qdrant_client,embedding_service,collection_name ):
            
        self.qdrant_client = qdrant_client
        self.embedding_service = embedding_service
        self.collection_name = collection_name

    def retrieve(self, question, n_chunk):
       query_embedding = self.embedding_service.embed(question) 
       results = self.qdrant_client.query_points(collection_name=self.collection_name, query=query_embedding, limit=n_chunk) 
       return [point.payload["text"] for point in results.points]

