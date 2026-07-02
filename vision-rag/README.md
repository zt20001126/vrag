# vision-rag

FastAPI skeleton for an image RAG knowledge base system.

This project is intentionally limited to an extensible engineering scaffold. It does not implement CLIP, Stable Diffusion, pgvector retrieval, or real database connectivity yet.

## Features

- Layered FastAPI structure
- Upload, search, and generate API placeholders
- Service layer boundaries for image handling, embeddings, and RAG retrieval
- SQLAlchemy model placeholder for future PostgreSQL and pgvector integration
- PgVector client placeholder
- Runnable JSON APIs for early integration testing

## Project Structure

```text
vision-rag/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── db/
│   ├── vector/
│   └── utils/
├── data/
│   └── uploads/
├── requirements.txt
├── .env
└── README.md
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

- `GET /health`
- `POST /api/v1/upload`
- `POST /api/v1/search`
- `POST /api/v1/generate`

## Future TODO

- TODO: Add CLIP image and text embedding implementation.
- TODO: Add PostgreSQL and pgvector connection management.
- TODO: Add vector search against persisted image embeddings.
- TODO: Add designer style metadata filtering.
- TODO: Add Stable Diffusion or another image generation backend.

## 运行方式

```
cd E:\Work\vrag\vision-rag
..\ .venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

