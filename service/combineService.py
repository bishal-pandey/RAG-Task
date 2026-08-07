from service.LLM import LLM
from service.retriever import Retrieval
from service.redis import MemoryService
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import dotenv
import os

QDRANT_API = os.getenv("QDRANT_API")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
QDRANT_HOST = os.getenv("QDRANT_HOST")



class CombineService:
    def __init__(self):
        self.llm = LLM()
        self.embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        self.client = QdrantClient(url="https://6b6aaed2-4c1d-4069-80c3-bbdbfad503b7.us-east-1-1.aws.cloud.qdrant.io",
                                                port=6333,
                                                api_key =QDRANT_API
                                                )
        self.retriever = Retrieval(qdrant_client=self.client, embedding_service=self.embedding,collection_name= QDRANT_COLLECTION)
        self.memory_service = MemoryService()

    def run_process(self,session_id, user_message):
        relevant_doc = self.retriever.retrieve(user_message, n_chunk=2)
        chat_history = self.memory_service.get_messages(session_id=session_id)

        llm_response = self.llm.conversation(user_message,chat_history,relevant_doc)

        self.memory_service.add_turn(
            session_id=session_id,
            user_msg=user_message,
            ai_msg=llm_response
        )

        return llm_response
