from fastapi import FastAPI

from app.db.database import engine, Base
from app.db.session import SessionLocal
from app.db.seed import seed_leads_if_empty
from app.api.leads import router as leads_router

app = FastAPI(
    title="EC3 Lead Management API",
    version="1.0.0",
    description="Simple Lead Management API for EC3 Technical Assessment",
)


@app.on_event("startup")
def startup_event():
    """
    Create database tables and seed mock data on startup.
    """
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_leads_if_empty(db)
    finally:
        db.close()


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(leads_router)
