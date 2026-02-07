import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingStore:
    """Lightweight vector store using all-MiniLM-L6-v2 (~80 MB) + FAISS.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", dim: int = 384):
        self.model = SentenceTransformer(model_name)
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.documents: list[dict] = []

    def add_documents(self, documents: list[dict]) -> None:
        """Add documents to the store.

        Each document should have at least ``{"text": "...", "source": "..."}``.
        """
        texts = [doc["text"] for doc in documents]
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        self.index.add(embeddings)
        self.documents.extend(documents)

    def query(self, query_text: str, top_k: int = 5) -> list[dict]:
        """Return the *top_k* most relevant documents for *query_text*."""
        query_vec = self.model.encode([query_text], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx, score in zip(indices[0], distances[0]):
            if 0 <= idx < len(self.documents):
                results.append({
                    **self.documents[idx],
                    "score": float(score),
                })
        return results

    def reset(self) -> None:
        """Clear the index and documents."""
        self.index.reset()
        self.documents.clear()
