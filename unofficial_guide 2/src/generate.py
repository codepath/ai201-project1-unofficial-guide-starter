"""
Grounded response generation for The Unofficial Guide.

Retrieves chunks, then instructs the LLM to answer ONLY from those chunks.
Source attribution is appended programmatically (not left to the model),
so it's guaranteed to be present and accurate even if the model forgets.
"""

import os
from groq import Groq
from dotenv import load_dotenv

from src.embed_store import query as retrieve_chunks

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are The Unofficial Guide, a Q&A assistant for Howard University \
campus dining knowledge.

STRICT RULES:
1. Answer ONLY using the information in the "Context" section below. Do not use \
any outside knowledge, even if you know it.
2. If the context does not contain enough information to answer, respond exactly: \
"I don't have enough information on that."
3. Do not speculate, generalize, or fill gaps with plausible-sounding guesses.
4. Keep your answer grounded in specific claims from the context — do not soften \
this into "students probably think..." style answers.
"""


def build_prompt(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )
    return f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"


def ask(question: str, k: int = 5) -> dict:
    """
    Full pipeline: retrieve -> generate -> attach sources.
    Returns {"answer": str, "sources": list[str], "chunks": list[dict]}
    """
    chunks = retrieve_chunks(question, k=k)

    # If retrieval comes back empty or all low-confidence, don't even call the LLM
    if not chunks or all(c["distance"] > 0.9 for c in chunks):
        return {
            "answer": "I don't have enough information on that.",
            "sources": [],
            "chunks": chunks,
        }

    prompt = build_prompt(question, chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    answer = response.choices[0].message.content.strip()

    # Programmatic source attribution — guaranteed correct regardless of what
    # the model says in its own text.
    unique_sources = sorted({c["source"] for c in chunks})

    return {"answer": answer, "sources": unique_sources, "chunks": chunks}


if __name__ == "__main__":
    result = ask("What do students say about the dining hall food?")
    print("ANSWER:", result["answer"])
    print("SOURCES:", result["sources"])
