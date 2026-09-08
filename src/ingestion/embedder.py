from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    embedding = model.encode(text)

    return embedding.tolist()


def embed_chunks(chunks: list[dict]) -> list[dict]:
    texts = [f"{chunk['heading']}\n{chunk['text']}" for chunk in chunks]

    embeddings = model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    return chunks
