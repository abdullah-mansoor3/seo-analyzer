# SEO Analyzer

A full-stack AI-powered application that crawls web pages for your selected site and uses AI to suggest SEO improvements you can make. It combines lightweight local embeddings with the Groq cloud API to deliver in-depth, actionable recommendations for every page — all runnable on modest hardware.

## Features

- **Web Crawler** — Recursively crawls your target website, extracting titles, meta descriptions, headings, links, structured data, and page content.
- **Rule-Based SEO Checks** — Instantly flags common issues: missing titles, long meta descriptions, multiple H1 tags, thin content, and lack of internal links.
- **RAG-Powered AI Analysis** — Embeds page data with a lightweight Sentence Transformer + FAISS running locally, then sends the retrieved context to Groq's blazing-fast cloud LLM for deep, prioritised SEO advice.
- **REST API** — FastAPI backend exposing a `POST /analyze` endpoint.
- **Animated React Frontend** — Modern dark-glass UI with gradient meshes, orbit loaders, step-progress pills, animated stat cards, tab panels, and staggered card reveals.
- **Docker Support** — Docker Compose for one-command backend deployment.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite 7 |
| Backend | Python 3.10+, FastAPI, Uvicorn |
| Crawler | Requests, BeautifulSoup4 |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2` — ~80 MB), FAISS |
| LLM | Groq cloud API (LLaMA 3.1 8B Instant — no local GPU needed) |
| Containerization | Docker, Docker Compose |

## Project Structure

```
seo-analyzer/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── crawler.py               # Web crawler (Requests + BeautifulSoup)
│   ├── rules_engine.py          # Rule-based SEO checks
│   ├── embeddings.py            # FAISS + Sentence Transformer vector store
│   ├── rag_engine.py            # RAG pipeline (embeddings → Groq API)
│   ├── report_generator.py      # Orchestrates rules + RAG into a report
│   └── apis/
│       └── seo_analyzer_api.py  # POST /analyze route
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css            # Full animated design system
│   │   ├── pages/Home.jsx
│   │   └── components/
│   │       ├── CrawlForm.jsx    # Form + results rendering
│   │       └── Loader.jsx       # Orbit loader with progress steps
│   ├── package.json
│   └── vite.config.js
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Prerequisites

- **Python** 3.10+
- **Node.js** 18+ and **npm**
- **Groq API key** — free at https://console.groq.com/keys
- **(Optional)** Docker & Docker Compose

> **No GPU required.** The only local model is the ~80 MB embedding model; the LLM runs on Groq's cloud.

---

## Setup & Run (Local)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd seo-analyzer
```

### 2. Backend Setup

#### a) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate          # Windows
```

#### b) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### c) Create a `.env` file in the project root

```bash
touch .env
```

Add your Groq API key:

```env
GROQ_API_KEY=gsk_your_key_here

# Optional — override the default model
# GROQ_MODEL=llama-3.1-8b-instant
```

Get a free key at https://console.groq.com/keys.

#### d) Start the backend

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify at http://localhost:8000 — you should see `{"status":"ok","service":"SEO Analyzer API"}`.

---

### 3. Frontend Setup

Open a **new terminal**:

```bash
cd frontend
npm install
npm run dev
```

The app will be at **http://localhost:5173**.

---

### 4. Using the App

1. Open http://localhost:5173.
2. Paste a website URL (e.g. `https://example.com`).
3. Click **Analyze**.
4. Watch the animated progress steps while the backend crawls, checks rules, builds embeddings, and queries the AI.
5. View results in two tabs: **AI Analysis** (Markdown report) and **Rule Checks** (per-page issues).

---

## Setup & Run (Docker)

### 1. Create `.env` in the project root (see step 2c above)

### 2. Build and start

```bash
cd docker
docker compose up --build
```

Backend will be at http://localhost:8000.

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Stop

```bash
cd docker
docker compose down
```

---

## API Reference

### `POST /analyze`

Crawl a site, run SEO checks, and return an AI-generated report.

**Request body:**

```json
{
  "url": "https://example.com",
  "query": "Give me detailed suggestions for improving SEO."
}
```

`query` is optional — a detailed default prompt is used if omitted.

**Response:**

```json
{
  "status": "success",
  "pages_crawled": 12,
  "report": {
    "rules_summary": { "checks": [ ... ] },
    "ai_analysis": "## Critical Issues\n...",
    "pages_analyzed": 12
  }
}
```

---

## License

This project is for educational and personal use.