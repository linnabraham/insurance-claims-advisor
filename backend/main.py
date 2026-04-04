"""FastAPI backend for the Claims Advisor application."""

from fastapi import FastAPI

app = FastAPI(
    title="Claims Advisor API",
    description="Insurance claim triage and decision support",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Simple health check to verify the API is running."""
    return {"status": "healthy", "service": "claims-advisor-api"}
