# RAG Engine API

A RAG (Retrieval Augmented Generation) engine built with FastAPI. Upload PDF documents, extract text via OCR, embed them into a vector database, and search semantically. Wrapped as an MCP server for AI agent integration.

## Tech Stack

- **FastAPI** — REST API
- **ChromaDB** — Vector database (no external server needed)
- **Mistral OCR** — Extract text from PDFs
- **LiteLLM** — Key points extraction (supports any provider)
- **Chonkie** — Semantic chunking
- **Celery + Redis** — Background processing
- **FastMCP** — MCP server wrapper

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker Desktop (for Redis)
- Mistral API key → [console.mistral.ai](https://console.mistral.ai)
- OpenRouter API key → [openrouter.ai](https://openrouter.ai)

## Setup

**1. Clone and install dependencies:**
```bash
git clone https://github.com/rafliogun49/assignment6-rag-engine-mcp.git
cd assignment6-rag-engine-mcp
uv sync
```

**2. Create `.env` file:**
```env
MISTRAL_API_KEY=your_mistral_api_key
KEY_POINTS_MODEL=openrouter/openai/gpt-4o-mini
KEY_POINTS_API_KEY=your_openrouter_api_key
REDIS_URL=redis://localhost:6379/0
```

**3. Start Redis:**
```bash
docker compose up -d
```

## Running

Open 3 terminals inside the project folder:

**Terminal 1 — FastAPI server:**
```bash
uv run uvicorn app.main:app --reload
```

**Terminal 2 — Celery worker:**
```bash
uv run celery -A app.celery_app worker --loglevel=info --pool=solo
```

**Terminal 3 — MCP server (optional):**
```bash
uv run python -m app.mcp_server
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/healthz` | Health check |
| `POST` | `/upload/` | Upload a PDF (processed in background) |
| `GET` | `/documents/` | List all documents |
| `GET` | `/documents/{doc_id}` | Get document + page list |
| `GET` | `/documents/{doc_id}/pages/{page_number}` | Get full page content |
| `GET` | `/search/?q=<query>&n=5` | Semantic search |

API docs available at: `http://localhost:8000/scalar`

## MCP Tools

When running as MCP server, two tools are exposed for AI agents:

- `search(query, n)` — Semantic search over indexed documents
- `get_page(doc_id, page_number)` — Fetch full page content

## How It Works

```
Upload PDF
  → Mistral OCR extracts text per page
  → LiteLLM extracts key facts (dates, names, numbers)
  → Chonkie splits key facts into semantic chunks
  → ChromaDB embeds and stores chunks

Search query
  → ChromaDB embeds query and finds closest chunks
  → Returns chunks with doc_id, page_number, distance
```
