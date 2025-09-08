"""
Configuration management for the Meeting Analysis API.
Updated for Pydantic v1 compatibility.
"""

import os
import logging
from functools import lru_cache
from typing import List

from pydantic import BaseSettings  # v1 import


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    APP_NAME: str = "Meeting Analysis API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Configuration
    OPENAI_API_KEY: str = ""
    ASSEMBLYAI_API_KEY: str = ""  # Optional alternative
    
    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # File handling
    MAX_FILE_SIZE: int = 25 * 1024 * 1024  # 25MB
    MAX_AUDIO_DURATION: int = 600  # 10 minutes
    SUPPORTED_FORMATS: str = "mp3,wav,mp4,m4a,ogg,flac"
    TEMP_DIR: str = "/tmp/meeting_analysis"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def supported_formats_list(self) -> List[str]:
        """Get supported formats as a list."""
        return [fmt.strip().lower() for fmt in self.SUPPORTED_FORMATS.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
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