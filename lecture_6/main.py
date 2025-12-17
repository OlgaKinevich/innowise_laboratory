"""
healthcheck_api.py

This module defines a simple FastAPI application with a healthcheck endpoint.
The healthcheck endpoint can be used to verify that the API service is running.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck() -> dict:
    """
    Healthcheck endpoint to verify that the API is running.

    Returns:
        dict: A dictionary containing the status of the service.
              Example: {"status": "ok"}
    """
    return {"status": "ok"}
