# ===== backend/app/utils/config.py (COMPLETE VERSION) =====
"""
Complete configuration management for the application.
"""

import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ASSEMBLYAI_API_KEY: str = ""  # Alternative transcription service
    
    # Application
    APP_NAME: str = "Meeting Analysis API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:8080,http://localhost:3000,http://localhost:5173"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert CORS origins string to list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # File processing
    MAX_FILE_SIZE: int = 26214400  # 25MB in bytes
    SUPPORTED_FORMATS: str = "mp3,wav,m4a,mp4,ogg,flac"
    TEMP_DIR: str = "/tmp/meeting_analysis"
    
    @property
    def supported_formats_list(self) -> List[str]:
        """Convert supported formats string to list."""
        return [fmt.strip().lower() for fmt in self.SUPPORTED_FORMATS.split(",")]
    
    # Processing limits
    MAX_CONCURRENT_JOBS: int = 3
    PROCESSING_TIMEOUT: int = 300  # 5 minutes
    MAX_AUDIO_DURATION: int = 600  # 10 minutes
    
    # OpenAI Configuration
    OPENAI_MODEL: str = "gpt-4o-mini"  # Cost-effective model
    WHISPER_MODEL: str = "whisper-1"   # OpenAI's hosted Whisper
    MAX_TRANSCRIPT_LENGTH: int = 4000  # Limit text sent to GPT (cost control)
    
    # Analysis limits (cost control)
    MAX_ACTION_ITEMS: int = 10
    MAX_KEY_DECISIONS: int = 5
    MAX_TOPICS: int = 5
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache settings (optional)
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour
    ENABLE_CACHING: bool = False
    
    # Database settings (optional)
    DATABASE_URL: str = "sqlite:///./meeting_analysis.db"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Feature flags
    ENABLE_SPEAKER_DIARIZATION: bool = True
    ENABLE_SENTIMENT_ANALYSIS: bool = True
    ENABLE_ACTION_ITEM_EXTRACTION: bool = True
    ENABLE_SUMMARIZATION: bool = True
    ENABLE_TOPIC_EXTRACTION: bool = True
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 10  # requests per minute
    RATE_LIMIT_WINDOW: int = 60   # window in seconds
    
    # Monitoring
    ENABLE_METRICS: bool = False
    METRICS_PORT: int = 8001
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables
    
    def validate_api_keys(self) -> bool:
        """Validate that required API keys are present."""
        if not self.OPENAI_API_KEY:
            return False
        if not self.OPENAI_API_KEY.startswith("sk-"):
            return False
        return True
    
    def get_temp_dir(self) -> str:
        """Get temp directory, creating if necessary."""
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        return self.TEMP_DIR
    
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.DEBUG
    
    def get_log_config(self) -> dict:
        """Get logging configuration."""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.LOG_FORMAT,
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": self.LOG_LEVEL,
                "handlers": ["default"],
            },
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# ===== backend/app/utils/__init__.py (COMPLETE VERSION) =====
"""
Utilities package for the Meeting Analysis API.
"""

from .config import get_settings, Settings
from .file_handler import (
    validate_audio_file,
    cleanup_temp_files,
    get_file_info,
    create_temp_directory,
    save_uploaded_file,
    get_safe_filename,
    estimate_processing_time,
    check_disk_space
)

__all__ = [
    "get_settings",
    "Settings",
    "validate_audio_file",
    "cleanup_temp_files", 
    "get_file_info",
    "create_temp_directory",
    "save_uploaded_file",
    "get_safe_filename",
    "estimate_processing_time",
    "check_disk_space"
]