"""
Chunking for The Unofficial Guide.

Strategy (edit these numbers + the reasoning in planning.md if you change them):
- Reviews are short and opinion-dense, so we chunk by paragraph/review boundary
  first (each review or comment usually IS one coherent thought).
- If a single paragraph is longer than CHUNK_SIZE characters (e.g. a long
  dining-hall policy page), we fall back to a sliding window with overlap so
  we don't lose context at the split point.

Defaults: CHUNK_SIZE=800 chars, OVERLAP=150 chars.
Tune these once you've looked at your actual documents (see hint in the
project instructions: short reviews want smaller chunks than long guides).
"""

CHUNK_SIZE = 800
OVERLAP = 150
MIN_CHUNK_LEN = 40  # discard tiny fragments (e.g. stray leftover lines)


def split_into_paragraphs(text: str) -> list[str]:
    """Split on blank lines / review boundaries."""
    paragraphs = [p.strip() for p in text.split("\n\n")]
    return [p for p in paragraphs if p]


def sliding_window(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Fallback fixed-window split with overlap, for long paragraphs."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def chunk_document(doc: dict) -> list[dict]:
    """
    Chunk a single {"source", "text"} document.
    Returns a list of {"source", "chunk_index", "text"} dicts.
    """
    chunks = []
    paragraphs = split_into_paragraphs(doc["text"])
    idx = 0

    for para in paragraphs:
        if len(para) <= CHUNK_SIZE:
            pieces = [para]
        else:
            pieces = sliding_window(para)

        for piece in pieces:
            piece = piece.strip()
            if len(piece) >= MIN_CHUNK_LEN:
                chunks.append({
                    "source": doc["source"],
                    "chunk_index": idx,
                    "text": piece,
                })
                idx += 1

    return chunks


def chunk_documents(docs: list[dict]) -> list[dict]:
    """Chunk a list of documents and return the flattened list of chunks."""
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc))

    print(f"Produced {len(all_chunks)} chunks from {len(docs)} documents.")
    return all_chunks


if __name__ == "__main__":
    from ingest import load_documents

    docs = load_documents("../documents") if __package__ else load_documents("documents")
    chunks = chunk_documents(docs)

    print("\n--- 5 sample chunks ---")
    for c in chunks[:5]:
        print(f"\n[{c['source']} | chunk {c['chunk_index']}]")
        print(c["text"][:300])
