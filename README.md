# CampusMind AI

CampusMind AI is an intelligent student success and academic assistant built as a full-stack project for academic planning, learning support, and career readiness.

## Stack

- Frontend: React + Vite + Tailwind CSS
- Backend: Python + FastAPI
- Database: PostgreSQL + SQLAlchemy
- Auth: JWT with password hashing
- AI: provider abstraction for LLM and embeddings
- Testing: Pytest
- Deployment: Docker + Docker Compose

## Monorepo layout

- `backend/` — FastAPI REST API and business logic
- `frontend/` — React dashboard and UI
- `docs/` — documentation and architecture notes
- `tests/` — repository-wide validation tests
- `docker-compose.yml` — local orchestration for app services
- `.env.example` — environment configuration template

## Local setup

1. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

4. Copy environment variables

```bash
copy .env.example .env
```

5. Start PostgreSQL and the services

```bash
docker-compose up --build
```

6. Run backend directly

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. Run frontend

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

## Backend tests

```bash
cd backend
pytest -q
```

## Frontend build

```bash
cd frontend
npm run build
```

## Notes

- Do not commit real API keys.
- Keep secrets in `.env` only.
- The app is structured for modular extension of AI tools, RAG, study planning, career support, and interviews.
