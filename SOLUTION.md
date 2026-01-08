# Solution Overview

## Architecture

This solution is implemented as a **FastAPI-based REST API** backed by **MariaDB** using **SQLAlchemy ORM**.  
The project follows a layered but intentionally lightweight structure suitable for an intermediate-level assessment.

**Key architectural decisions:**
- **FastAPI** selected as per assessment requirements.
- **SQLAlchemy ORM (sync)** used for simplicity and transparency over async complexity.
- **MariaDB** selected as per assessment requirements.
- **Pydantic schemas** used to strictly separate API contracts from database models.
- **Startup lifecycle hooks** used for table creation and mock data seeding.

---

## Project Structure (Conceptual)

- `app/main.py` – Application entry point and lifecycle management
- `app/api/` – API route definitions (Leads CRUD + report)
- `app/models/` – SQLAlchemy ORM models
- `app/schemas/` – Pydantic request/response schemas
- `app/db/` – Database engine, session handling, and seed logic
- `database/` – SQL reference script for schema verification
- `app/postman/` – Postman collection and environment

---

## Assumptions

- The assessment focuses primarily on **backend API design**, not frontend delivery.
- A **single-database, single-service** architecture is sufficient.
- Authentication and authorization are **out of scope**.
- MariaDB is running locally and accessible via credentials configured in code.
- CSV reporting is sufficient for export requirements.

---

## Tradeoffs

### Simplicity vs Extensibility
- A service/repository layer was intentionally **not introduced** to avoid over-engineering.
- CRUD logic lives directly in route handlers for clarity and traceability.

### Sync vs Async Database Access
- Synchronous SQLAlchemy was chosen for stability and ease of reasoning.
- Async SQLAlchemy would add complexity without meaningful benefit for this scope.

### Environment Configuration
- Database connection string is defined directly rather than via environment variables.
- This favors ease of setup over production-level configuration management.

---

## Error Handling & Logging

- Centralized logging added for:
  - Application startup/shutdown
  - Request lifecycle (method, path, status, timing, request ID)
  - Expected errors (e.g. 404 Not Found)
- Errors return structured JSON responses including a `request_id` for traceability.
- SQLAlchemy engine logging enabled for visibility during assessment review.

---

## AI Usage

AI (ChatGPT) was used as a **development assistant**, specifically to:
- Bridge the knowledge gap since I am unfamiliar with Python, FastAPI, or MariaDB.
- Produce Code under strict guidance from myself to achieve certain functionality.
- Validate FastAPI and SQLAlchemy best practices.
- Help structure project layout and naming conventions.
- Review error handling and logging approaches.
- Sanity-check architectural decisions.

---

## Validation & Testing

- Endpoints tested via **Postman**
- CRUD operations validated against live MariaDB data
- CSV report endpoint validated with filtered and unfiltered exports
- Startup seeding verified to be idempotent

---

## Future Improvements (Out of Scope)

- Environment-based configuration (`.env`, secrets management)
- Authentication & authorization
- Async DB layer or connection pooling tuning
- Automated tests (pytest)
- Pagination metadata and HATEOAS-style responses

---
