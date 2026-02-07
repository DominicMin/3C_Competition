from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB, Load Models, etc.
    print("Startup: Satu-Sama AI Backend")
    yield
    # Shutdown
    print("Shutdown: Cleanup")

app = FastAPI(
    title="Satu-Sama AI Backend",
    description="Compliance-as-a-Service for Malaysia E-commerce",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Satu-Sama AI"}

@app.get("/")
async def root():
    return {"message": "Welcome to Satu-Sama AI Backend API. Visit /docs for Swagger UI."}
