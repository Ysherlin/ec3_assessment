# EC3 Lead Management API

A simple Lead Management REST API built with **FastAPI**, **Python**, and **MariaDB** for the EC3 Full Stack Developer Technical Assessment.

This project demonstrates clean API design, database integration, validation, logging, and basic reporting.

---

## Tech Stack

- Python 3.14  
- FastAPI  
- SQLAlchemy  
- MariaDB  
- Pydantic  
- Uvicorn  
- Postman (API testing)

---

## Features

- CRUD operations for Leads  
- Input validation using Pydantic  
- Pagination and filtering  
- CSV report export endpoint  
- Startup database seeding (mock data)  
- Structured logging with request IDs  
- Centralised error handling  
- Health check endpoint  

---

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup the Database

Run the SQL script:

```text
database/Leads.sql
```

This script:
- Creates the database `ec3_leads_db`
- Creates the `leads` table

---

### 4. Configure Database Connection

Edit the file:

```text
app/db/database.py
```

Example connection string:

```text
mysql+pymysql://root:password@localhost:3306/ec3_leads_db
```

---

### 5. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

API Base URL:
```text
http://127.0.0.1:8000
```

Swagger UI:
```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health
- `GET /health`

### Leads
- `POST   /leads`
- `GET    /leads`
- `GET    /leads/{id}`
- `PUT    /leads/{id}`
- `DELETE /leads/{id}`

### Reports
- `GET /leads/report`  
  Downloads a CSV report of leads.

---

## CSV Report Filters

The `/leads/report` endpoint supports the following optional query parameters:

- `from_date` (YYYY-MM-DD)
- `to_date` (YYYY-MM-DD)
- `name` (partial match)
- `email` (exact match)
- `source` (partial match)

---

## Postman

Postman files are included in the repository:

- `EC3 Leads API.postman_collection.json`
- `EC3 Local.postman_environment.json`

Import both files into Postman to test the API locally.

---

## Notes

- Mock data is automatically seeded on application startup if the database is empty.
- Logging includes request IDs for easier traceability.
- Docker was intentionally not used as it was not required by the assessment.

---

## Author

Ysherlin Govender
078 701 2565
