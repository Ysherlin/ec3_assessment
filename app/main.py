from fastapi import FastAPI

from app.db.database import engine, Base
from app.api.leads import router as leads_router

app = FastAPI(
    title="EC3 Lead Management API",
    version="1.0.0",
    description="Simple Lead Management API for EC3 Technical Assessment",
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(leads_router)
