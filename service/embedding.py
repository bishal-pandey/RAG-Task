from sentence_transformers import SentenceTransformer

#shape (2,384)
class Embedding:
    def __init__(self, model_name = "sentence-transformers/all-MiniLM-L6-v2"):
        # 1. Load a pretrained Sentence Transformer model
        self.model = SentenceTransformer(model_name)

    def transform(self, texts):
        if not texts:
            return []
        embedding = self.model.encode(texts)
        return embedding


