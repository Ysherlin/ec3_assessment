import os
import logging
from fastapi import FastAPI

from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.exceptions import register_exception_handlers

from app.db.database import engine, Base
from app.db.session import SessionLocal
from app.db.seed import seed_leads_if_empty
from app.api.leads import router as leads_router

# Configure logging as early as possible
configure_logging(os.getenv("LOG_LEVEL", "INFO"))

logger = logging.getLogger("app")


app = FastAPI(
    title="EC3 Lead Management API",
    version="1.0.0",
    description="Simple Lead Management API for EC3 Technical Assessment",
)

# Middleware
app.add_middleware(RequestLoggingMiddleware)

# Exception handlers
register_exception_handlers(app)


@app.on_event("startup")
def startup_event():
    """
    Create database tables and seed mock data on startup.
    """
    logger.info("Starting application...")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        inserted = seed_leads_if_empty(db)
        if inserted > 0:
            logger.info("Seeded %s lead(s) into database.", inserted)
        else:
            logger.info("Database already has data; seeding skipped.")
    finally:
        db.close()

    logger.info("Startup completed.")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(leads_router)
