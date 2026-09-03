# Planning

<!--
⚠️ Fill this in yourself — the assignment explicitly says not to have an AI
tool write this content for you. Use AI to pressure-test your reasoning, not
to generate it. The code in src/ already implements defaults (CHUNK_SIZE=800,
OVERLAP=150, k=5) — your job here is to justify (or change) those numbers
based on the documents you actually collected.
-->

## Domain
[What domain did you choose? Why is this knowledge valuable and hard to find
through official channels? (Campus dining — 2-3 sentences on why official
Howard dining pages don't tell you what students actually think.)]

## Documents
[List your 10 specific sources — URLs, subreddit threads, Yelp pages, file
descriptions. Note which are short reviews vs. longer guide/policy pages.]

## Chunking Strategy
[State chunk size and overlap (the code defaults to 800 chars / 150 overlap)
and explain why those numbers fit YOUR documents. If your reviews are much
shorter or longer than that, say so and adjust CHUNK_SIZE in src/chunking.py.]

## Retrieval Approach
[Embedding model: all-MiniLM-L6-v2 via sentence-transformers. Top-k: 5
(default in src/embed_store.py). What tradeoffs would you weigh for a
production embedding model — cost, context length, multilingual support,
local vs. API?]

## Evaluation Plan
[Your 5 test questions with specific, verifiable expected answers. Make them
concrete enough that a grader could check your system's response against a
clear right answer.]

1.
2.
3.
4.
5.

## Anticipated Challenges
[At least two specific risks: noisy documents, missing attribution, off-topic
retrieval, chunks splitting key info across boundaries, etc.]

## AI Tool Plan
[Which parts of the pipeline did you use AI to help implement? Be specific
about what you gave it as input and what you got back. Example already true
for this project: "I used Claude to generate src/ingest.py, src/chunking.py,
src/embed_store.py, src/generate.py, and app.py from this planning.md spec
and the assignment's pipeline diagram requirement. I reviewed the grounding
prompt in generate.py and confirmed source attribution is appended
programmatically rather than left to the model."]

## Architecture

```
Document Ingestion (src/ingest.py)
        |
        v
   Chunking (src/chunking.py)  -- paragraph-based, 800 char / 150 overlap
        |
        v
Embedding + Vector Store (src/embed_store.py)
   - all-MiniLM-L6-v2 (sentence-transformers)
   - ChromaDB (persistent, local)
        |
        v
   Retrieval (src/embed_store.py: query())  -- top-k = 5
        |
        v
   Generation (src/generate.py)
   - Groq: meta-llama/llama-4-scout-17b-16e-instruct
   - Grounded prompt + programmatic source attribution
        |
        v
   Query Interface (app.py — Gradio)
```
