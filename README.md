# Anime Semantic Search Engine

> Find anime by meaning, not just keywords. Search _"a sword-wielding mc set in feudal Japan"_ and get results that actually understand you.

A full-stack semantic search engine powered by NLP vector embeddings. Instead of matching exact keywords, it encodes the _contextual meaning_ of a user's query and finds anime with semantically similar descriptions using cosine similarity.

---

## Tech Stack

| Layer              | Technology                                    |
| ------------------ | --------------------------------------------- |
| Frontend           | React (Vite)                                  |
| Backend API        | C# (ASP.NET Core Web API)                     |
| ML / Data Pipeline | Python, HuggingFace `sentence-transformers`   |
| Vector Database    | Qdrant / Pinecone / PostgreSQL / tbd          |
| Data Source        | [Jikan API](https://jikan.moe/) (MyAnimeList) |

---

## Architecture Overview

```
User Query
    │
    ▼
React Frontend  ──(HTTP)──▶  C# ASP.NET Core API
                                      │
                          Embed query with HuggingFace model
                                      │
                                      ▼
                             Vector Database
                          cosine similarity search
                                      │
                                      ▼
                             Top-N anime results
                                      │
                                      ▼
                             React Frontend renders cards
```

**How it works end-to-end:**

1. **Data Ingestion** — A Python script fetches anime metadata (title, synopsis, genres) from the Jikan API.
2. **Vectorization** — Each synopsis is encoded into a high-dimensional embedding vector using a pre-trained `sentence-transformers` model, capturing its semantic meaning.
3. **Vector Storage** — Embeddings and metadata are upserted into a vector database, enabling fast approximate nearest-neighbor lookups.
4. **Semantic Search** — When a user submits a query, the C# API embeds it using the same model and runs a cosine similarity search against the stored vectors, returning the closest matches.

---

## Roadmap

### Infrastructure

- [x] Project structure and multi-language `.gitignore`

### Data Pipeline (Python)

- [ ] Jikan API scraper — fetch top 1000 anime
- [ ] HuggingFace embedding generation (`all-MiniLM-L6-v2`)
- [ ] Upsert embeddings into vector database

### Backend (C# / ASP.NET Core)

- [ ] Initialize .NET Web API project
- [ ] Connect to vector database client
- [ ] `POST /api/search` — embed query and run similarity search
- [ ] Return ranked results with metadata

### Frontend (React)

- [ ] Search bar component with query submission
- [ ] Anime result cards (title, synopsis, score, cover image)
- [ ] Loading states and error handling
- [ ] Responsive layout

---

## License

[MIT](LICENSE)
