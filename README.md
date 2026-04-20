# geologic-time-scale-api
A FastAPI-based REST API for exploring the geologic time scale hierarchy (eons, eras, periods, epochs, ages).  
The project includes a SQLite database, seed data loader, and export functionality.

---

## Features

* Hierarchical representation of geologic time units
* Parent/child relationships
* Unit metadata (name, rank, time range)
* Duration and short description
* Export data to CSV and to JSON
* Seed system based on JSON files
* SQLite database (local development)

---

## Tech Stack

* Python 3.14+
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn

---

## Project Structure

```
app/
  main.py

  config/         # environment configuration
  database/       # SQLAlchemy engine, session, DB file
  models/         # ORM models
  schemas/        # Pydantic schemas
  routers/        # API endpoints
  seed/           # database seeding from JSON
  utils/          # helper functions (formatters)
  exports/        # generated files (CSV, etc.)
```

---

## Setup

### 1. Clone repository
```bash
git clone https://github.com/smsln93/geologic-time-scale-api.git
```
### 2. Create virtual environment
```bash
cd geologic-time-scale-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure environment
Create `.env` file:

```dotenv
API_KEY=your-key
API_BASE_URL=http://127.0.0.1:8000/geologic-time-scale-api/v1
DATABASE_URL=sqlite:///./app/database/data/geologic-time-scale-app.db
```
### 5. Run application
```bash
uvicorn app.main:app --reload
```

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

## Database Seeding

The database is populated with chronostratigraphic data stored in JSON files located in the `app/seed/input` directory.

---

This project was built to demonstrate and practice backend development skills using FastAPI, with a focus on real-world architecture and data handling.

Key objectives:

* Designing and building RESTful APIs with FastAPI
* Applying clean, layered architecture principles
* Modeling hierarchical data structures
* Implementing database seeding from structured data sources
* Organizing modular API structure using routers
* Exporting structured data in a usable format
* Writing automated tests for API reliability
* Working with realistic, domain-driven datasets

---

## Roadmap / TODO

* [x] Add full CRUD endpoints for chronostratigraphic units
* [x] Extend input JSON dataset with additional chronostratigraphic units
* [ ] Implement automated tests (unit and integration)
* [ ] Add Docker support for containerized deployment
* [ ] Introduce `pyproject.toml` for project configuration and dependency management

---

## License

MIT
