# geologic-time-scale-api
A FastAPI-based REST API for exploring the geologic timescale hierarchy (eons, eras, periods, epochs, ages).
The project includes a SQLite database and data export functionality.

---

## Features

- hierarchical representation of geologic time units
- parent/child relationships between units
- unit metadata (name, rank, time range, duration, description)
- data export to CSV and JSON
- optional database seeding via JSON-based script
- SQLite database for local development
- automated pytest-based test suite
- dockerized setup with Docker Compose (API + testing environment)
- CI integration via GitHub Actions

---

## Objectives

This project implements a backend system for managing and serving geologic timescale data using FastAPI and SQLAlchemy.

Key objectives:

- model hierarchical geologic time as a relational dataset
- expose structured geological data through a RESTful API
- optional dataset initialization via script using JSON files
- validate system correctness through automated testing

---

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Database ORM:** SQLAlchemy
- **Data validation:** Pydantic
- **Testing:** Pytest, HTTPX
- **Configuration:** python-dotenv

---

## Project Structure

```
app/
  main.py

  core/           # environment configuration loader
  database/       # SQLAlchemy engine, session, DB file
  enums/          # domain-level enumerations
  models/         # ORM models
  routers/        # API endpoints
  schemas/        # Pydantic schemas
  services/       # data export service
  utils/          # helper functions (formatters)

scripts/          # database seeding from JSON (standalone script)
exports/          # generated files (CSV, etc.)
tests/            # automated tests (pytest)

run.py            # application entrypoint used to start API locally
pytest.ini        # pytest configuration
.env              # local environment variables (not committed)
.env.example      # template for required configuration
requirements.txt  # project dependencies
Dockerfile        # container image definition
.dockerignore     # ignored files for Docker build
compose.yaml      # docker compose setup
```

---

## Setup

### Clone repository
```bash
git clone https://github.com/smsln93/geologic-time-scale-api.git
cd geologic-time-scale-api
```
### Configure environment
Create `.env` file:

```dotenv
API_KEY=your-key
API_BASE_URL=http://127.0.0.1:8000/geologic-time-scale-api/v1
DATABASE_URL=sqlite:///./app/database/data/geologic-time-scale-app.db
```
You can also use example file:
```bash
cp .env.example .env
```
---

## Run application

### Build and start API with Docker
```bash
docker compose up --build
```
API will be available at:
```
http://127.0.0.1:8000/geologic-time-scale-api/v1/
```
Run tests (Docker):
```bash
docker compose run --rm api pytest
```

### Local development (without Docker)
Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run application:
```bash
python run.py
```
Alternatively, you can run it directly with Uvicorn:
```bash
uvicorn app.main:app --reload
```

---

## Testing

The project uses pytest to ensure correctness of API behavior, data processing, and export functionality.

### Test scope

- geological time calculations and data consistency
- REST API endpoints (units, exports)
- CSV export validation
- general application behavior

### Run tests

```bash
pytest
```
### Test structure
```
tests/
  conftest.py         # shared fixtures (DB, client, env)
  settings.py         # shared test configuration
  export/             # CSV/JSON export validation
  units/              # API tests for geological time units
  utils/              # helpers and custom assertions
```

### Notes
- Test environment variables are overridden using pytest fixtures
- Each test runs with a clean database state

---

## CI / GitHub Actions

The test suite is automatically executed on every push and pull request to ensure code quality and stability.

---

## Database
The project uses a local SQLite database (`app/database/data/geologic-time-scale-app.db`) 
containing data based on the International Chronostratigraphic Chart (v2024-12).

---

## Database rebuild script

This project includes a utility script for rebuilding and seeding the database from scratch.

It is intended for local development and testing purposes only.

### Functionality

- drops and recreates the database schema
- seeds initial data from JSON files

### Usage

```bash
python -m scripts.rebuilt_database --db-url sqlite:///./scripts/test.db 
````
**Warning**
This script will overwrite existing data.

---
## API Documentation

After running the server:

- Swagger UI:
  `http://127.0.0.1:8000/geologic-time-scale-api/v1/docs`

- ReDoc:
  `http://127.0.0.1:8000/geologic-time-scale-api/v1/redoc`

---

## Example API Endpoints

### Get all units (public)
```
GET /units
```
Optional filters:
```
GET /units?rank=Period&parent_id=pharenozoic
GET /units?at_time=100
GET /units?before=250&after=100

Filters `before` and `after` use strict inequalities (<, >).
Values equal to the boundary are excluded.

```
### Get unit by ID (public)
```
GET /units/mesozoic
```

### Get unit duration (public)
```
GET /units/triassic/duration
```

To use secure endpoints (POST, PUT, PATCH, DELETE), you must define an API key in your `.env` file:
```dotenv
API_KEY=your_secret_api_key
```
Without API key configured, write operations will not be available or will be rejected by the server (HTTP 403).
Remember to include the key in request headers:
```bash
X-API-Key: your_secret_api_key
```

### Create unit (requires API key)
```
POST /units

Headers:
  X-API-Key: your_api_key
Body:
{
"id": "jurassic",
"name": "Jurassic",
"rank": "Period",
"rank_order": 4,
"parent_id": "mesozoic",
"begin_time_ma": 201.3,
"begin_uncertainty_ma": 0.2,
"end_time_ma": 145.0,
"end_uncertainty_ma": 0.2
}
```

### Update unit (requires API key)
```
PUT /units/jurassic

Headers:
  X-API-Key: your_api_key
Body:
{
  "id": "jurassic"
  "name": "Jurassic",
  "rank": "Period",
  "rank_order": 4,
  "parent_id": "mesozoic",
  "begin_time_ma": 201.3,
  "begin_uncertainty_ma": 0.2,
  "end_time_ma": 145.0,
  "end_uncertainty_ma": 0.2
}
```
```
PATCH /units/jurassic

Headers:
  X-API-Key: your_api_key
Body:
{
"name": "Jurassic"
}
```

### Delete unit (requires API key)
```
DELETE /units/hadean
Headers:
  X-API-Key: your_api_key
```

### Export data (public)
```
GET /export/csv
GET /export/json
```
Exported files are generated and stored in the `/exports` directory.

---

## Roadmap / TODO

- [x] Add full CRUD endpoints for chronostratigraphic units
- [x] Extend input JSON dataset with additional chronostratigraphic units
- [x] Implement automated tests (unit and integration)
- [x] Add working script that will be used to initialize the database with predefined data
- [x] Add Docker support for containerized deployment
- [ ] Introduce `pyproject.toml` for project configuration and dependency management

---

## License

MIT
