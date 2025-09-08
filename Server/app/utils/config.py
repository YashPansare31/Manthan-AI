"""
Simple configuration management - no BaseSettings needed.
"""

import os
from functools import lru_cache
from typing import List


class Settings:
    """Simple settings class using environment variables."""
    
    def __init__(self):
        # Application settings
        self.APP_NAME = "Meeting Analysis API"
        self.APP_VERSION = "1.0.0"
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        
        # API Configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")
        
        # Server settings
        self.HOST = os.getenv("HOST", "127.0.0.1")
        self.PORT = int(os.getenv("PORT", "8000"))
        self.ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
        
        # File handling
        self.MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
        self.MAX_AUDIO_DURATION = 600  # 10 minutes
        self.SUPPORTED_FORMATS = "mp3,wav,mp4,m4a,ogg,flac"
        self.TEMP_DIR = "/tmp/meeting_analysis"
        
        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def supported_formats_list(self) -> List[str]:
        """Get supported formats as a list."""
        return [fmt.strip().lower() for fmt in self.SUPPORTED_FORMATS.split(",")]
    
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