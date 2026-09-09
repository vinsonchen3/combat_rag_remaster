from sentence_transformers import SentenceTransformer
import chromadb


class Retriever:
    def __init__(self, collection, model, top_k=3):
        self.collection = collection
        self.model = model
        self.top_k = top_k

    def retrieve(self, query: str) -> list[dict]:
        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
        )

        output = []
        for document, metadata in zip(
            results["documents"][0],
            results["metadatas"][0],
        ):
            output.append({"text": document, "metadata": metadata})

        return output
