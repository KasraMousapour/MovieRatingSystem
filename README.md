# Movie Rating System

A movie rating system built with FastAPI, PostgreSQL.The project involves designing and implementing a backend system that maintains and manages information about movies, directors, genres, and user ratings. The data stored in a PostgreSQL database and the necessary operations performed through FastAPI-based APIs.In this project for two endpoints have written logging.

## 🏗️ Architecture

The project follows a clean/hexagonal architecture:

```
┌─────────────────────────────────────────┐
│         FastAPI API Layer               │
│  (Routes, Pydantic schemas, deps)       │
└─────────────────────────────────────────┘
              ▲
              │
┌─────────────────────────────────────────┐
│    Application / Services Layer         │
│  (Business logic, use cases)            │
└─────────────────────────────────────────┘
              ▲
              │
┌─────────────────────────────────────────┐
│    Repository / Data Access Layer       │
│  (Database operations, abstractions)    │
└─────────────────────────────────────────┘
              ▲
              │
┌─────────────────────────────────────────┐
│         Database (PostgreSQL)           │
└─────────────────────────────────────────┘
```

## 📁 Project Structure

```
app/
├── api/                    # FastAPI routes and dependencies
│   └── controllers/
|       ├── config/
|       |   └── logging.conf
|       └── movie_controller.py
|   ├── controllers_schemas/   # Pydantic request/response schemas
|   |   ├── director_schema.py
|   |   ├── genre_schema.py
|   |   └── movie_schema.py
|   ├── __init__.py
│   ├── routers.py      # API endpoints
│   └── deps.py        # Dependency injection
├── models/                # SQLAlchemy ORM models
│   ├── director.py
│   ├── genre.py
│   ├── movie_genre.py
│   ├── movie_rating.py
│   └── movie.py
├── repositories/          # Data access layer with interfaces
│   ├── director_repository.py
│   ├── genre_repository.py
│   ├── movie_repository.py
│   └── ...
├── services/              # Business logic layer
│   └── movie_service.py
├── db/
│   ├── base.py           # SQLAlchemy base
│   └── session.py        # Session management
├── scripts/
|   └── seed_check.py
└── main.py               # FastAPI application
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Poetry (Python package manager)
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Seed the database**
   
   After manual PostgreSQL setup in docker for seeding run
   ```bash
    psql -U <username>-d <db_name> -h localhost -f scripts/seeddb.sql
   ```
   for test successfully added data to database run `scripts/seed_check.py`

4. **Run migrations**
   ```bash
   poetry run alembic upgrade head
   ```

5. **Run the application**
   ```bash
   poetry run uvicorn ticketer.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   
   API documentation: `http://localhost:8000/docs`