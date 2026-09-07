from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    embedding = model.encode(text)

    return embedding.tolist()


def embed_document(document: list[dict]) -> list[dict]:
    texts = [f"{chunk['heading']}\n{chunk['text']}" for chunk in document]

    embeddings = model.encode(texts)

    for document, embedding in zip(document, embeddings):
        document["embedding"] = embedding.tolist()

    return document
