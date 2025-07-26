"""
Complete production FastAPI main application.
"""

import os
import logging
import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import analyze
from app.utils.file_handler import cleanup_temp_files
from app.utils.config import get_settings

# Get settings
settings = get_settings()

# Configure logging
logging.config.dictConfig(settings.get_log_config())
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    
    # Startup
    logger.info("🚀 Starting Meeting Analysis API...")
    logger.info(f"📊 Version: {settings.APP_VERSION}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    
    # Validate configuration
    try:
        # Check API keys
        if not settings.validate_api_keys():
            logger.error("❌ OpenAI API key validation failed!")
            logger.error("Please set OPENAI_API_KEY environment variable")
            if not settings.DEBUG:
                raise RuntimeError("Invalid API configuration")
        else:
            logger.info("✅ OpenAI API key validated")
        
        # Create temp directory
        temp_dir = settings.get_temp_dir()
        logger.info(f"📁 Temp directory: {temp_dir}")
        
        # Check disk space
        import shutil
        disk_usage = shutil.disk_usage(temp_dir)
        available_gb = disk_usage.free / (1024**3)
        logger.info(f"💾 Available disk space: {available_gb:.1f} GB")
        
        if available_gb < 1.0:
            logger.warning("⚠️ Low disk space available!")
        
        logger.info("✅ API started successfully")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        if not settings.DEBUG:
            raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Meeting Analysis API...")
    try:
        cleanup_temp_files()
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered meeting transcription and analysis service using OpenAI APIs",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
    # Custom OpenAPI metadata
    contact={
        "name": "Meeting Analysis API",
        "url": "https://github.com/yourusername/meeting-analysis",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Security middleware (production only)
if settings.is_production():
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*"]  # Configure with your actual domains in production
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Custom exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle request validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred" if settings.is_production() else str(exc)
        }
    )

# Include routers
app.include_router(analyze.router, prefix="/api", tags=["analysis"])

# Root endpoints
@app.get("/")
async def root():
    """API root endpoint with basic information."""
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs" if settings.DEBUG else "disabled",
        "endpoints": {
            "analyze": "/api/analyze",
            "health": "/health",
            "status": "/api/status"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    
    Returns:
        Service health status and dependencies
    """
    try:
        # Check critical dependencies
        import time
        
        health_status = {
            "status": "healthy",
            "timestamp": int(time.time()),
            "version": settings.APP_VERSION,
            "services": {
                "openai_api": settings.validate_api_keys(),
                "temp_directory": os.path.exists(settings.get_temp_dir()),
                "disk_space_available": True  # Could add actual check
            },
            "configuration": {
                "debug_mode": settings.DEBUG,
                "max_file_size_mb": settings.MAX_FILE_SIZE / 1024 / 1024,
                "max_audio_duration": settings.MAX_AUDIO_DURATION,
                "supported_formats": len(settings.supported_formats_list)
            }
        }
        
        # Check if any critical service is down
        critical_services = ["openai_api", "temp_directory"]
        if not all(health_status["services"][service] for service in critical_services):
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": int(time.time()),
            "error": str(e) if settings.DEBUG else "Health check failed"
        }

@app.get("/info")
async def api_info():
    """
    Get detailed API information and capabilities.
    """
    return {
        "api": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "AI-powered meeting transcription and analysis"
        },
        "capabilities": {
            "transcription": "OpenAI Whisper API",
            "analysis": {
                "summarization": settings.ENABLE_SUMMARIZATION,
                "action_items": settings.ENABLE_ACTION_ITEM_EXTRACTION,
                "sentiment": settings.ENABLE_SENTIMENT_ANALYSIS,
                "topics": settings.ENABLE_TOPIC_EXTRACTION,
                "decisions": True
            }
        },
        "limits": {
            "max_file_size": f"{settings.MAX_FILE_SIZE / 1024 / 1024:.1f} MB",
            "max_duration": f"{settings.MAX_AUDIO_DURATION} seconds",
            "supported_formats": settings.supported_formats_list,
            "max_action_items": settings.MAX_ACTION_ITEMS,
            "max_decisions": settings.MAX_KEY_DECISIONS,
            "max_topics": settings.MAX_TOPICS
        },
        "pricing": {
            "model": "Pay-per-use via OpenAI API",
            "transcription": "$0.006 per minute",
            "analysis": "Based on GPT-4o-mini usage"
        }
    }

# Development only endpoints
if settings.DEBUG:
    @app.get("/debug/settings")
    async def debug_settings():
        """Debug endpoint to view current settings (development only)."""
        return {
            "note": "This endpoint is only available in debug mode",
            "settings": {
                "app_name": settings.APP_NAME,
                "debug": settings.DEBUG,
                "openai_key_configured": bool(settings.OPENAI_API_KEY),
                "max_file_size": settings.MAX_FILE_SIZE,
                "temp_dir": settings.TEMP_DIR,
                "cors_origins": settings.allowed_origins_list,
                "supported_formats": settings.supported_formats_list
            }
        }
    
    @app.post("/debug/test-api")
    async def debug_test_api():
        """Test OpenAI API connectivity (development only)."""
        try:
            import httpx
            
            # Test simple API call
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
                )
                
                if response.status_code == 200:
                    return {"status": "success", "message": "OpenAI API is accessible"}
                else:
                    return {"status": "error", "message": f"API returned {response.status_code}"}
                    
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Add startup event logging
@app.on_event("startup")
async def startup_event():
    """Additional startup logging."""
    logger.info("🎯 Meeting Analysis API is ready to process files!")
    if settings.DEBUG:
        logger.info(f"📚 API documentation available at: /docs")
        logger.info(f"🔍 Debug endpoints available at: /debug/*")