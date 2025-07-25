from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import aiofiles
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List
import logging

from ..models.schemas import AnalysisResponse, ActionItem, Decision, Speaker
from ..services.audio_processor import AudioProcessor
from ..services.nlp_analyzer import NLPAnalyzer

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize processors
audio_processor = AudioProcessor()
nlp_analyzer = NLPAnalyzer()

ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm', '.mp4'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_file(file: UploadFile = File(...)):
    """
    Analyze uploaded audio file for meeting insights
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process audio
            logger.info(f"Processing audio file: {file.filename}")
            audio_results = await audio_processor.process_audio(temp_file_path)
            
            # Perform NLP analysis
            logger.info("Performing NLP analysis")
            nlp_results = await nlp_analyzer.analyze_transcript(
                audio_results["transcript"],
                audio_results.get("speakers", [])
            )
            
            # Combine results
            analysis_result = AnalysisResponse(
                transcript=audio_results["transcript"],
                speakers=audio_results.get("speakers", []),
                action_items=nlp_results.get("action_items", []),
                decisions=nlp_results.get("decisions", []),
                key_topics=nlp_results.get("key_topics", []),
                sentiment_analysis=nlp_results.get("sentiment", {}),
                summary=nlp_results.get("summary", ""),
                confidence_score=nlp_results.get("confidence", 0.0),
                processing_time=audio_results.get("processing_time", 0) + nlp_results.get("processing_time", 0)
            )
            
            logger.info("Analysis completed successfully")
            return analysis_result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/formats")
async def get_supported_formats():
    """Get list of supported file formats"""
    return {
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "max_file_size_mb": MAX_FILE_SIZE // (1024*1024)
    }