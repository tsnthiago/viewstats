# ViewStats

## 📚 Project Overview

**ViewStats** is an AI-powered web platform that performs semantic video classification and search. It processes a dataset of over **124,000 YouTube videos**, extracting custom hierarchical topics and enabling **semantic exploration** through a full-stack application.

This solution includes:
- AI-generated **multi-label classification** for each video and channel
- A **hierarchical taxonomy** of topics and subtopics
- A **semantic search engine** powered by vector embeddings and Qdrant
- A basic **FastAPI backend** and optional frontend for navigation and exploration

---

## 🔧 Technologies Used

- **Backend**: FastAPI (Python)
- **Vector Database**: Qdrant
- **Containerization**: Docker Compose
- **Text Processing**: Pandas, Sentence Transformers, BERTopic
- **Embeddings**: `all-MiniLM-L6-v2` (or equivalent)
- **Optional**: React/Next.js frontend

---

## 🧠 Core Features

### ✅ Semantic Video Indexing
- Embeddings generated from video title, description, and full transcript
- Optional transcript pre-processing and lemmatization
- Storage of vectorized representations in Qdrant
- Metadata (e.g., views, duration, channel info) stored as payload

### ✅ Custom Topic Modeling
- Automatic extraction of topics using topic modeling and clustering
- Derivation of a **multi-level hierarchical taxonomy**
- Multi-label classification at both **video** and **channel** levels
- No reliance on pre-defined categories — taxonomy is emergent from content

### ✅ Intelligent Semantic Search
- Vector similarity search using Qdrant
- Support for context-aware keyword queries (e.g., `"Magnus Carlsen"` → chess)
- API endpoints to support free-text search and topic-based exploration

### ✅ API & Taxonomy Browser
- Backend exposes:
  - `/search`: vector-based semantic search
  - `/taxonomy`: hierarchical topic explorer
  - `/video/{id}`: individual video metadata
  - `/channel/{id}`: channel-level topic labels and info

---

## 📁 Project Structure

```

viewstats/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       └── services/
│           ├── file\_processor.py
│           └── embedding\_engine.py
├── docker-compose.yaml

````

---

## 🚀 How to Run

### 1. Start the Application
```bash
docker-compose up --build
````

### 2. Access

* Backend API: [http://localhost:8000](http://localhost:8000)
* Qdrant UI/API: [http://localhost:6333](http://localhost:6333)

---

## 🧪 API Endpoints

| Endpoint        | Method | Description                        |
| --------------- | ------ | ---------------------------------- |
| `/`             | GET    | Health check                       |
| `/upload-csv`   | POST   | Upload CSV, return file metadata   |
| `/search`       | POST   | Semantic search (vector + keyword) |
| `/taxonomy`     | GET    | Explore hierarchical taxonomy      |
| `/video/{id}`   | GET    | Retrieve video metadata            |
| `/channel/{id}` | GET    | Retrieve channel classification    |

---

## 🎯 Evaluation Criteria (from challenge)

| Area                         | Weight |
| ---------------------------- | ------ |
| Classification Accuracy      | 30%    |
| Semantic Search Relevance    | 30%    |
| Backend/API Design           | 15%    |
| Frontend Functionality       | 10%    |
| Code Quality & Documentation | 10%    |

✅ **Bonus Points** included for:

* Context-aware abbreviations (e.g., NBA ↔ National Basketball Association)
* Autocomplete suggestions
* Topic co-occurrence graphs
* Filtered/faceted UI

---

## 📦 Dependencies

* Python 3.11 (Dockerized)
* `fastapi`, `uvicorn`, `pandas`
* `sentence-transformers`, `qdrant-client`
* `BERTopic` or other topic modeling tools

---

## 🔒 Notes

* This project is provided under **NDA** and must not be shared publicly.
* The system is designed to operate within a 24–48 hour build window.
* Optional expenses may be covered up to \$100 — list any used APIs and receipts in the write-up.

---

## 📝 Deliverables

* ✅ Source code (backend + frontend if built)
* ✅ This README with setup, architecture and design decisions
* ✅ Commentary on modeling, limitations, and assumptions
* ✅ (Optional) Loom or screenshots
* ✅ (Optional) Deployed link (not required)

---

## 🧭 Future Extensions

* Add frontend UI (React, SvelteKit, etc.)
* Autocomplete and search suggestions
* RAG-based search augmentation
* Analytics and visualizations on topic distributions

---

## 📬 Submission

Send your GitHub repo and documentation to:

* [nagesh@mrbeastyoutube.com](mailto:nagesh@mrbeastyoutube.com)
* [byronm@mrbeastyoutube.com](mailto:byronm@mrbeastyoutube.com)
* [nicolas@viewstats.com](mailto:nicolas@viewstats.com)

---

## © License

This project is provided solely for evaluation purposes under NDA.