"""
Run once to build (or rebuild) the vector store from documents/.

    python build_index.py
"""

from src.ingest import load_documents
from src.chunking import chunk_documents
from src.embed_store import add_chunks

if __name__ == "__main__":
    docs = load_documents("documents")
    chunks = chunk_documents(docs)

    print("\n--- 5 sample chunks (copy these into README Sample Chunks) ---")
    for c in chunks[:5]:
        print(f"\n[{c['source']} | chunk {c['chunk_index']}]")
        print(c["text"][:300])

    print(f"\nTotal chunks: {len(chunks)}")
    if len(chunks) < 50:
        print("⚠️  Fewer than 50 chunks — consider whether your chunks are too large.")
    if len(chunks) > 2000:
        print("⚠️  More than 2000 chunks — consider whether your chunks are too small.")

    add_chunks(chunks)
    print("\n✅ Index built. Run app.py to query it.")
