"""FastAPI backend for the Claims Triage and Decision Support application."""

from fastapi import FastAPI

app = FastAPI(
    title="Claims Triage and Decision Support API",
    description="Insurance claim triage and decision support",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Simple health check to verify the API is running."""
    return {"status": "healthy", "service": "claims-triage-and-decision-support-api"}
