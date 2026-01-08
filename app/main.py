from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import Lead

app = FastAPI(
    title="EC3 Lead Management API",
    version="1.0.0",
    description="Simple Lead Management API for EC3 Technical Assessment"
)


@app.on_event("startup")
def startup_event():
    """
    Create database tables on application startup.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
