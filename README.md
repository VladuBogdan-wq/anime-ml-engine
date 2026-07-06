# Anime Semantic Search Engine

> Find anime by meaning, not just keywords. Search _"a slow-burn romance set in feudal Japan"_ and get results that actually understand you.

A full-stack semantic search engine powered by NLP vector embeddings. Instead of matching exact keywords, it encodes the _contextual meaning_ of a user's query and finds anime with semantically similar descriptions using cosine similarity.

---

## Tech Stack

| Layer                  | Technology                                    |
| ---------------------- | --------------------------------------------- |
| Frontend               | React (Vite) + Tailwind CSS                   |
| Backend API            | C# (ASP.NET Core Web API)                     |
| ML / Data Pipeline     | Python, HuggingFace `sentence-transformers`   |
| ML Inference (runtime) | ONNX Runtime for .NET                         |
| Vector Database        | Qdrant (Docker)                               |
| Data Source            | [Jikan API](https://jikan.moe/) (MyAnimeList) |

---

## Architecture Overview

```
User Query
    │
    ▼
React Frontend  ──(HTTP)──▶  C# ASP.NET Core API
                                      │
                          Embed query via ONNX Runtime
                          (all-MiniLM-L6-v2, 384 dims)
                                      │
                                      ▼
                             Qdrant Vector Database
                          cosine similarity search
                                      │
                                      ▼
                             Top-N anime results
                             (title, synopsis, genres, score)
                                      │
                                      ▼
                             React Frontend renders cards
```

**How it works end-to-end:**

1. **Data Ingestion** — A Python script fetches anime metadata (title, synopsis, genres) from the Jikan API.
2. **Vectorization** — Each synopsis is encoded into a 384-dimensional embedding vector using `all-MiniLM-L6-v2`, capturing its semantic meaning.
3. **Vector Storage** — Embeddings and metadata are upserted into a Qdrant collection, enabling fast cosine similarity lookups.
4. **ONNX Export** — The HuggingFace model is exported to ONNX format so it can run natively inside the C# API at inference time.
5. **Semantic Search** — When a user submits a query, the C# API embeds it using the ONNX model, runs a cosine similarity search against the stored vectors, and returns the closest matches.

---

## Roadmap

### Completed

- [x] Project structure and multi-language `.gitignore`
- [x] Jikan API scraper — fetch top anime
- [x] HuggingFace embedding generation (`all-MiniLM-L6-v2`)
- [x] Qdrant vector database setup and upload
- [x] ONNX model export for C# runtime inference
- [x] `POST /api/search` — embed query and run cosine similarity search
- [x] React frontend — search bar, result cards, loading/error states
- [x] Tailwind CSS dark theme UI

### Upcoming

#### Scale to Full Dataset

The current dataset covers ~100 anime. MyAnimeList has ~25,000 entries. Scaling up requires:

- Pagination strategy across the full Jikan API dataset
- Batch embedding generation to handle memory efficiently
- Benchmarking Qdrant query performance at scale and tuning index parameters (HNSW settings) if needed

#### Cover Images

- Fetch and store MAL cover image URLs alongside existing metadata in the Jikan scraper (the `images` field is already returned by the API)
- Display cover images on anime result cards in the React frontend

#### Weighted Attribute Search

Currently the search query is embedded as a single block of text. The goal is to support **priority tags** — for example, searching _"sword wielding mc with red hair"_ should weight "sword wielding mc" higher than "red hair".

- Explore multi-field embeddings or query decomposition strategies
- Potentially embed synopsis, genres, and visual attributes as separate vectors and combine scores at query time

#### Watched Anime Filter

- Allow users to maintain a local "watched" list
- Exclude watched anime from search results at query time using Qdrant's payload filtering feature (filter by `mal_id` not in watched list)
- This doubles as a performance optimization at scale — filtering before ranking reduces the candidate set Qdrant needs to score

---

## License

[MIT](LICENSE)
