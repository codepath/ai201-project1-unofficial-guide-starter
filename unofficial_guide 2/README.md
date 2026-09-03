# The Unofficial Guide — Howard University Dining

## Domain and Documents
[Domain summary + list of your 10 sources with names/URLs — copy from planning.md]

## Chunking Strategy
[Chunk size, overlap, and why — copy from planning.md. Code default:
CHUNK_SIZE=800 chars, OVERLAP=150, paragraph-first with sliding-window
fallback for long documents. See src/chunking.py.]

## Sample Chunks
<!-- Run `python build_index.py` and paste 5 of the printed chunks here -->

**Chunk 1** (source: `___.txt`)
```
[paste]
```

**Chunk 2** (source: `___.txt`)
```
[paste]
```

**Chunk 3** (source: `___.txt`)
```
[paste]
```

**Chunk 4** (source: `___.txt`)
```
[paste]
```

**Chunk 5** (source: `___.txt`)
```
[paste]
```

## Embedding Model
Model: `all-MiniLM-L6-v2` (sentence-transformers), local, no API key.

Production tradeoffs: [your reflection — cost, context length, multilingual
support, local vs. API. e.g. a larger API-based model like OpenAI's
text-embedding-3-large would likely improve retrieval on nuanced phrasing but
adds per-query cost and network latency; a multilingual model matters if the
dining reviews come from a mixed-language student body, which is worth
considering for a real HBCU deployment.]

## Retrieval Test Results
<!-- Run 3 of your eval questions through src/embed_store.py's query() and
paste results here. For at least 2, explain why the returned chunks are
relevant. -->

**Query 1:** [question]
- Top chunk (source, distance): [paste]
- Why relevant: [explanation]

**Query 2:** [question]
- Top chunk (source, distance): [paste]
- Why relevant: [explanation]

**Query 3:** [question]
- Top chunk (source, distance): [paste]

## Grounded Generation
Grounding is enforced via the system prompt in `src/generate.py`, which
instructs the model to answer only from retrieved context and to say "I
don't have enough information on that" otherwise. Source attribution is
appended **programmatically** from chunk metadata (not left to the model),
so citations are guaranteed accurate even if the model's own text omits them.

**Example response 1:**
[paste question + answer + sources]

**Example response 2:**
[paste question + answer + sources]

**Out-of-scope example (system correctly declines):**
[paste a question your documents don't cover + the "I don't have enough
information" response]

## Query Interface
Gradio web UI (`app.py`). Input: a free-text question box. Output: an
"Answer" box (grounded response) and a "Retrieved from" box (source
filenames). Sample transcript:

```
Q: [question]
A: [answer]
Sources: [sources]
```

## Evaluation Report
| # | Question | Expected Answer | System Response | Judgment |
|---|----------|-----------------|------------------|----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Failure case:** [Which question failed, and a specific pipeline-level
explanation — not "the answer was wrong" but e.g. "the relevant sentence was
split across the paragraph boundary in chunking.py's sliding window, so
neither retrieved chunk contained the full claim."]

## Spec Reflection
- One way planning.md helped: [...]
- One way implementation diverged from the spec, and why: [...]

## AI Usage
1. [What you asked an AI tool to do, e.g. "Generate src/embed_store.py from
   my Retrieval Approach section" — what it produced, what you changed.]
2. [Second instance.]

## Demo Video
[Link] — 3–5 min, showing 3+ queries with citations, one good retrieval, one
failure case, and a walkthrough of the evaluation report.
