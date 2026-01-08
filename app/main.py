from fastapi import FastAPI

app = FastAPI(
    title="EC3 Lead Management API",
    version="1.0.0",
    description="Simple Lead Management API for EC3 Technical Assessment"
)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok"}
