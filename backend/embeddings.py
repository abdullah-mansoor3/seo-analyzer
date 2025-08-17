import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingStore:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", dim=384):
        self.model = SentenceTransformer(model_name)
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)  # L2 distance index
        self.text_store = []  # keep original text alongside embeddings

    def add_documents(self, documents):
        """
        documents: list of dicts with keys {id, text, meta}
        """
        texts = [doc["text"] for doc in documents]
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        self.index.add(embeddings)
        self.text_store.extend(documents)

    def query(self, query_text, top_k=5):
        """
        query_text: str
        return: list of top-k (text, meta, score)
        """
        query_vec = self.model.encode([query_text], convert_to_numpy=True)
        D, I = self.index.search(query_vec, top_k)

        results = []
        for idx, score in zip(I[0], D[0]):
            if idx < len(self.text_store):
                results.append({
                    "text": self.text_store[idx]["text"],
                    "meta": self.text_store[idx]["meta"],
                    "score": float(score)
                })
        return results
