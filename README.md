# Task API

A REST API for managing tasks, built with FastAPI and PostgreSQL. Includes full JWT authentication with refresh token rotation, user authorization and a complete set of automated tests.

## Why I built this
I wanted a portfolio project that goes beyond basic CRUD tutorials. I wanted to build something that reflects the kind of backend work I'd actually be doing in an internship, with proper authentication, authorization, testing and Docker instead of just endpoints that read and write to a database.

## Live Demo
[Live API docs](https://task-api-rlvt.onrender.com/docs)

Note: hosted on Render's free tier, so the app may take up to a minute to wake up after being inactive.

## Screenshots
**API documentation overview**
![API docs overview](docs/screenshots/api-docs-overview.png)

**Creating a task — request**
![Create task request](docs/screenshots/create-task-request.png)

**Creating a task — response**
![Create task response](docs/screenshots/create-task-response.png)

**Test suite passing**
![Tests passing](docs/screenshots/tests-passing.png)

## Features

- **JWT authentication** — registration, login and refresh token rotation with separate access/refresh token
- **User authorization** — every task belongs to a specific user; users can only view, edit, or delete their own tasks
- **Password security** — Argon2 password hashing using `pwdlib`
- **Rate limiting** — login endpoint protected against brute-force attempts
- **Filtering & sorting** — filter tasks by completion status and sort them by different fields
- **Database migrations** — schema changes are managed with Alembic instead of creating tables manually
- **Fully async** — SQLAlchemy 2.0 with `AsyncSession` throughout the application
- **Automated tests** — 12 tests covering authentication, CRUD and authorization edge cases, using a separate test database to keep test data isolated
- **Docker** — one command starts the API and database together
- **Interactive API docs** — auto-generated Swagger UI at `/docs`.

## Tech stack

- **Framework:** FastAPI
- **Database:** PostgreSQL, SQLAlchemy 2.0 (async), Alembic
- **Auth:** PyJWT, pwdlib (Argon2)
- **Validation:** Pydantic v2
- **Testing:** pytest, pytest-asyncio, httpx
- **Tooling:** uv, ruff
- **Containerization:** Docker, Docker Compose

## Getting started

### Prerequisites

- Docker and Docker Compose

### Setup

1. Clone the repository:
```bash
   git clone https://github.com/Acosta381/task-api.git
   cd crud
```

2. Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql+asyncpg://postgres:1234@localhost:5432/taskdb
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=taskdb
```

3. Start the app and database:
```bash
   docker compose up --build
```

4. In a new terminal, run the database migrations:
```bash
   docker compose exec api /app/.venv/bin/alembic upgrade head
```

5. Open the interactive API docs:
http://localhost:8000/docs

**Interactive API documentation:** This project uses FastAPI's built-in Swagger UI, automatically available at `/docs` once running. You can explore every endpoint, view request/response schemas and test calls directly from your browser.

## Running tests

Tests run against a separate PostgreSQL database and are fully isolated from development data.

```bash
uv sync --dev
uv run pytest
```

## API overview

Full interactive documentation (with request/response schemas and a live "Try it out" console) is available at `/docs` once the app is running. Key endpoints:

**Auth**
- `POST /auth/login` — log in and returns access and refresh tokens (rate-limited)
- `POST /auth/refresh` — exchange a refresh token for a new access and refresh token pair

**Users**
- `POST /users/register` — create an account

**Tasks** (all require authentication)
- `GET /tasks/` — list your tasks (filter by completion status and sort them by different fields)
- `POST /tasks/` — create a task
- `GET /tasks/{id}` — get a single task
- `PATCH /tasks/{id}` — update a task
- `DELETE /tasks/{id}` — delete a task

## Project structure

```text
├── core/               # config, security (hashing/JWT), rate limiter, auth dependency
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic request/response schemas
├── crud/               # database access logic
├── routers/            # API endpoints
├── migration/          # Alembic migrations
├── tests/              # pytest suite
├── main.py             # app entry point
└── docker-compose.yml  # Docker Compose configuration
```