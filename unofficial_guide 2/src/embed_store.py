"""
Embedding + vector store for The Unofficial Guide.

Embeds chunks locally with sentence-transformers (all-MiniLM-L6-v2) and
stores them in a persistent ChromaDB collection with source metadata.

Usage:
    python build_index.py     # builds the index once
    from src.embed_store import get_collection, add_chunks, query
"""

import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
DB_PATH = "chroma_db"
COLLECTION_NAME = "unofficial_guide"

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_chunks(chunks: list[dict]):
    """Embed and store a list of {"source", "chunk_index", "text"} chunks."""
    collection = get_collection()
    model = get_model()

    texts = [c["text"] for c in chunks]
    ids = [f"{c['source']}::{c['chunk_index']}" for c in chunks]
    metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

    print(f"Embedding {len(texts)} chunks with {MODEL_NAME}...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    # Chroma errors on duplicate ids across runs, so reset the collection first
    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    print(f"Stored {len(texts)} chunks in ChromaDB collection '{COLLECTION_NAME}'.")


def query(question: str, k: int = 5) -> list[dict]:
    """Return the top-k most relevant chunks for a query, with distances."""
    collection = get_collection()
    model = get_model()

    query_embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)

    hits = []
    for text, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({
            "text": text,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": distance,
        })
    return hits


if __name__ == "__main__":
    # Quick manual test after build_index.py has been run once
    test_query = "What do students say about the dining hall food?"
    for hit in query(test_query, k=3):
        print(f"\n[{hit['source']} | dist={hit['distance']:.3f}]")
        print(hit["text"][:300])
