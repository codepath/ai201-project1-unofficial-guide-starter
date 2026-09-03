"""
Document ingestion for The Unofficial Guide.

Loads every .txt file from documents/, strips common web/HTML noise,
and returns a list of {"source": filename, "text": cleaned_text} dicts.

Usage:
    from src.ingest import load_documents
    docs = load_documents("documents")
"""

import os
import re
import html


NOISE_PATTERNS = [
    r"Write a review.*?Suggest an edit",   # Yelp boilerplate
    r"People searched for.*?business\.",
    r"Share\s*·\s*Save",
    r"<[^>]+>",                            # stray HTML tags
]


def clean_text(raw: str) -> str:
    """Strip HTML entities, boilerplate, and excess whitespace from raw text."""
    text = html.unescape(raw)

    for pattern in NOISE_PATTERNS:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE | re.DOTALL)

    # Collapse repeated whitespace/newlines left over from cleaning
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    return text


def load_documents(folder: str = "documents") -> list[dict]:
    """Load every .txt file in `folder`, clean it, and return structured docs."""
    docs = []

    if not os.path.isdir(folder):
        raise FileNotFoundError(
            f"'{folder}' not found. Create it and add your .txt source documents."
        )

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()

        cleaned = clean_text(raw)

        if len(cleaned) == 0:
            print(f"⚠️  Warning: {filename} produced empty text after cleaning.")
            continue

        docs.append({"source": filename, "text": cleaned})

    print(f"Loaded {len(docs)} documents from '{folder}'.")
    return docs


if __name__ == "__main__":
    documents = load_documents()
    if documents:
        print("\n--- Sample cleaned document ---")
        print(documents[0]["source"])
        print(documents[0]["text"][:500])
