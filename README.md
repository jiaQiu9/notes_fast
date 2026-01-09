# Notes FastAPI / Knowledge Base API

````markdown


## Project Description

**Notes FastAPI** is a backend API designed to help users organize notes, links, and media files in a centralized system. It provides endpoints for creating, reading, updating, and deleting notes, and allows users to associate each note with related links and media resources.  

This project is cross-platform and containerized, making it easy to run on any system with **Docker**. It uses **FastAPI** as the web framework, **PostgreSQL** as the database, **SQLAlchemy** for ORM, and **Alembic** for database migrations.  

Whether for personal note-taking or building a small knowledge base, this API provides a structured and scalable solution.

---

## Key Features

- CRUD operations for notes, links, and media  
- Associate notes with links and media files  
- Database migrations with Alembic  
- Containerized setup for easy deployment on local machines or cloud servers  
- Interactive API documentation via FastAPI  

---

## Tech Stack

- **Backend Framework:** FastAPI  
- **Database:** PostgreSQL  
- **ORM / Migrations:** SQLAlchemy + Alembic  
- **Containerization:** Docker + Docker Compose  
- **Testing:** Pytest  

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<USERNAME>/notes_fast.git
cd notes_fast
````

### 2. Create and configure the `.env` file

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following variables (adjust values if needed):

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/kb_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=kb_db
```

**Explanation of variables:**

* `DATABASE_URL` → SQLAlchemy connection string
* `POSTGRES_USER` → Postgres username
* `POSTGRES_PASSWORD` → Postgres password
* `POSTGRES_DB` → Postgres database name

> Make sure these match your `docker-compose.yml`.

---

### 3. Start Docker containers

```bash
docker compose up -d
```

* Starts the Postgres database and FastAPI API container
* `-d` runs containers in the background

Check running containers:

```bash
docker ps
```

**Expected output (example):**

```
CONTAINER ID   IMAGE               COMMAND                  STATUS          PORTS
abcd1234       notes_fast-api      "uvicorn app.main:ap…"   Up 10s          0.0.0.0:8000->8000/tcp
efgh5678       postgres:15        "docker-entrypoint.s…"   Up 10s          0.0.0.0:5432->5432/tcp
```

---

### 4. Apply database migrations

Generate and apply initial database tables:

```bash
docker compose exec api alembic upgrade head
```

Verify tables:

```bash
docker compose exec db psql -U postgres -d kb_db -c "\dt"
```

**Expected output:**

```
       List of relations
 Schema |     Name      | Type  | Owner
--------+---------------+-------+--------
 public | alembic_version | table | postgres
 public | notes          | table | postgres
 public | users          | table | postgres
 ...
```

---

### 5. Run the FastAPI server (if not using Docker)

Activate the Python virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be accessible at:

```
http://localhost:8000
```

---

### 6. Access the API documentation

FastAPI provides interactive documentation:

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

---

## Example API Calls

**1. Create a new note**

```bash
curl -X POST "http://localhost:8000/notes/" \
-H "Content-Type: application/json" \
-d '{
  "title": "My First Note",
  "content": "This is a sample note",
  "user_id": 1
}'
```

**2. Get all notes**

```bash
curl -X GET "http://localhost:8000/notes/"
```

**3. Get a single note by ID**

```bash
curl -X GET "http://localhost:8000/notes/1"
```

**4. Update a note**

```bash
curl -X PUT "http://localhost:8000/notes/1" \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Note Title",
  "content": "Updated content"
}'
```

**5. Delete a note**

```bash
curl -X DELETE "http://localhost:8000/notes/1"
```

---

## Docker Compose Notes

* `docker compose up -d` → start all services (API + DB)
* `docker compose down` → stop all containers
* `docker compose exec api bash` → open a terminal inside the API container
* `docker compose exec db psql -U postgres -d kb_db` → open Postgres CLI

---

## Quick Start / Command Checklist

Copy and paste the following commands in sequence to get the project running:

```bash
# 1. Clone the repository
git clone https://github.com/<USERNAME>/notes_fast.git
cd notes_fast

# 2. Create the .env file with default environment variables
cat > .env <<EOL
DATABASE_URL=postgresql://postgres:postgres@db:5432/kb_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=kb_db
EOL

# 3. Build and start Docker containers (API + Postgres)
docker compose up -d

# 4. Apply database migrations
docker compose exec api alembic upgrade head

# 5. Verify database tables
docker compose exec db psql -U postgres -d kb_db -c "\dt"

# 6. (Optional) Enter API container shell
docker compose exec api bash

# 7. Access the API in your browser or with cURL
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

**Optional manual Python setup (if not using Docker):**

```bash
# Activate Python virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Stop all Docker containers when finished:**

```bash
docker compose down
```

```

---

This README is **fully self-contained**, professional, and ready to copy into GitHub.  

- ✅ `.env` setup included  
- ✅ Docker instructions included  
- ✅ Example API calls included  
- ✅ Quick Start / command checklist included  


