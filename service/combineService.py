from LLM import LLM
from retriever import Retrieval
from redis import MemoryService
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class CombineService:
    def __init__(self):
        self.llm = LLM()
        self.embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        self.client = QdrantClient(url="https://6b6aaed2-4c1d-4069-80c3-bbdbfad503b7.us-east-1-1.aws.cloud.qdrant.io",
                                                port=6333,
                                                api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6Y2YzZjRkYWEtZGQ2YS00MDUwLWEwZDEtM2NhODM1YmU1MDNkIn0.HW5BydHlwKvR0YsWwZBpvlJi7ff-LgdJX1BLd3EVqMw"
                                                )
        self.retriever = Retrieval(qdrant_client=self.client, embedding_service=self.embedding, collection_name="ingestion_api")
        self.memory_service = MemoryService()

    def run_process(self,session_id, user_message):
        relevant_doc = self.retriever.retrieve(user_message, n_chunk=5)
        chat_history = self.memory_service.get_messages(session_id=session_id)

        llm_response = self.llm.conversation(user_message,chat_history,relevant_doc)

        self.memory_service.add_turn(
            session_id=session_id,
            user_msg=user_message,
            ai_msg=llm_response
        )
