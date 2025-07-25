from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import List, Dict, Any
import aiofiles
import tempfile
from pathlib import Path

from .routers import analyze
from .models.schemas import AnalysisResponse

app = FastAPI(
    title="Meeting Analysis API",
    description="Audio file analysis with ASR and NLP processing",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, prefix="/api/v1", tags=["analysis"])

@app.get("/")
async def root():
    return {"message": "Meeting Analysis API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "meeting-analysis-api"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )