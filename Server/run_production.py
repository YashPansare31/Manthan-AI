"""
Production server runner for Meeting Analysis API.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Production configuration
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))
    
    print(f"🚀 Starting Meeting Analysis API (Production)")
    print(f"🌐 Server: {host}:{port}")
    print(f"👥 Workers: {workers}")
    print(f"🔧 Debug: false")
    
    # Run with production settings
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        workers=workers,
        reload=False,
        log_level="info",
        access_log=True
    )