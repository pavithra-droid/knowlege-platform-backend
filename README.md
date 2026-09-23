# Knowledge Platform Backend

A Django REST API for building a personal knowledge platform where users can upload documents and ask questions about their documents using **Retrieval-Augmented Generation (RAG)**.

## Tech Stack

* Python 3.13
* Django + Django REST Framework
* PostgreSQL
* Redis
* Celery
* Sentence Transformers
* Vector/Semantic Search
* LLM API
* Docker Compose
* uv

## Architecture

```text
                         ┌──────────────┐
                         │   Django API │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
         Authentication    Documents API      Chat API
                                │                 │
                                ▼                 ▼
                              Celery          RAGService
                                │                 │
                                ▼          ┌──────┼──────┐
                         Chunk + Embed      │      │      │
                                           ▼      ▼      ▼
                                      Search  Prompt   LLM
                                      Service Builder Service
                                           │
                                           ▼
                                      PostgreSQL
```

## RAG Flow

### Document ingestion

```text
Upload Document
      ↓
Django API
      ↓
Celery Task
      ↓
Extract Text
      ↓
Chunk Document
      ↓
Generate Embeddings
      ↓
Store Chunks + Embeddings
```

### Question answering

```text
User Question
      ↓
Generate Question Embedding
      ↓
Semantic Search
      ↓
Top 5 Relevant Chunks
      ↓
PromptBuilder
      ↓
LLMService
      ↓
Answer
```

The retrieved chunks are provided to the LLM as context so that answers are based on the user's documents.

## Project Structure

```text
backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
│
├── documents/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   └── services/
│       ├── search.py
│       └── ...
│
├── ai/
│   └── services/
│       ├── rag.py
│       ├── prompt.py
│       └── llm.py
│
├── manage.py
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── docker-compose.yml
```

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd knowledge-platform-backend/backend
```

### 2. Configure environment variables

Create `.env`:

```env
SECRET_KEY=your-django-secret-key

POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppass
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

OPENAI_API_KEY=your-api-key
OPENAI_MODEL=your-model
```

### 3. Start the services

From the project directory:

```bash
docker compose up --build
```

Services:

```text
Django      → http://localhost:8000
PostgreSQL  → localhost:5432
Redis       → localhost:6379
```

### 4. Run migrations

```bash
docker compose exec web uv run python manage.py migrate
```

### 5. Create a superuser

```bash
docker compose exec web uv run python manage.py createsuperuser
```

### 6. Start Celery worker

In another terminal:

```bash
docker compose exec web uv run celery -A config worker -l info
```

## API Flow

### Authentication

```text
POST /api/auth/register/
POST /api/auth/login/
```

### Documents

```text
POST /api/documents/
GET  /api/documents/
GET  /api/documents/<id>/
```

Upload a document using `multipart/form-data`.

Example:

```text
title       = Django Guide
description = Django documentation
files       = django.pdf
```

The document is processed asynchronously by Celery.

### Chat

```text
POST /api/chat/
```

Request:

```json
{
    "question": "How does Django authentication work?"
}
```

Response:

```json
{
    "answer": "Django authentication provides...",
    "sources": [...]
}
```

## Main Components

### SearchService

Responsible for semantic search and retrieving the most relevant document chunks.

### PromptBuilder

Creates the prompt using:

* system instructions
* retrieved document context
* user's question

### LLMService

Responsible only for communicating with the LLM.

The client is injected into the service so it can easily be mocked during testing.

### RAGService

Coordinates the complete RAG workflow:

```text
Search
  ↓
Retrieve chunks
  ↓
Build prompt
  ↓
Call LLM
  ↓
Return answer
```

## Why RAG?

Instead of sending the entire document to the LLM, the application retrieves only the relevant chunks.

This reduces:

* token usage
* latency
* irrelevant context

and allows the LLM to answer questions using private user documents.

## Future Improvements

* Conversation history
* Streaming responses
* Source citations
* Hybrid search
* Reranking
* Query rewriting
* Redis caching
* Rate limiting
* LLM retry with exponential backoff
* Monitoring and metrics
