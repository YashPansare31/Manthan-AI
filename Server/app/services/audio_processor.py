"""
Complete production audio processor for API-based transcription.
Handles audio preprocessing and format conversion for OpenAI Whisper API.
"""

import os
import tempfile
import asyncio
import logging
from typing import Optional

from pydub import AudioSegment
import librosa
import soundfile as sf

from app.utils.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ProductionAudioProcessor:
    """Production audio processor - handles basic audio preprocessing for API transcription."""
    
    def __init__(self):
        """Initialize audio processor."""
        self.target_sample_rate = 16000  # Optimal for Whisper API
        self.max_duration = 600  # 10 minutes max for single API call
        self._ready = True
        logger.info("Production Audio Processor initialized")
    
    def is_ready(self) -> bool:
        """Check if service is ready."""
        return self._ready
    
    async def process_audio(self, file_path: str, session_id: str) -> str:
        """
        Process audio file for optimal API transcription.
        
        Args:
            file_path: Path to input audio file
            session_id: Session identifier for output naming
            
        Returns:
            Path to processed audio file
        """
        try:
            logger.info(f"Processing audio file: {file_path}")
            
            # Validate input file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Audio file not found: {file_path}")
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > settings.MAX_FILE_SIZE:
                raise ValueError(f"File too large: {file_size} bytes")
            
            # Run processing in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            processed_path = await loop.run_in_executor(
                None, 
                self._process_audio_sync,
                file_path,
                session_id
            )
            
            logger.info(f"Audio processing completed: {processed_path}")
            return processed_path
            
        except Exception as e:
            logger.error(f"Audio processing failed: {str(e)}")
            # Return original file if processing fails (better than crashing)
            return file_path
    
    def _process_audio_sync(self, file_path: str, session_id: str) -> str:
        """Synchronous audio processing implementation."""
        
        # Create output directory
        output_dir = tempfile.mkdtemp(prefix="audio_proc_")
        output_path = os.path.join(output_dir, f"{session_id}_processed.wav")
        
        try:
            # Try librosa first for better quality
            logger.debug("Attempting librosa processing")
            audio, sr = librosa.load(file_path, sr=self.target_sample_rate)
            
            # Validate audio data
            if len(audio) == 0:
                raise ValueError("Empty audio data")
            
            # Normalize audio to prevent clipping
            audio = librosa.util.normalize(audio)
            
            # Check duration and split if too long
            duration = len(audio) / sr
            if duration > self.max_duration:
                logger.warning(f"Audio duration {duration:.1f}s exceeds maximum {self.max_duration}s")
                # Truncate to max duration
                max_samples = int(self.max_duration * sr)
                audio = audio[:max_samples]
            
            # Save processed audio
            sf.write(output_path, audio, sr)
            
            # Verify output file was created
            if not os.path.exists(output_path):
                raise RuntimeError("Failed to create output file")
            
            logger.debug(f"Librosa processing successful: {output_path}")
            return output_path
            
        except Exception as e:
            logger.warning(f"Librosa processing failed: {e}, trying pydub fallback")
            # Fallback to pydub
            return self._fallback_conversion(file_path, output_path)
    
    def _fallback_conversion(self, input_path: str, output_path: str) -> str:
        """Fallback audio conversion using pydub."""
        try:
            logger.debug("Attempting pydub fallback conversion")
            
            # Load audio with pydub (supports more formats)
            audio = AudioSegment.from_file(input_path)
            
            # Convert to mono and set sample rate
            audio = audio.set_channels(1)
            audio = audio.set_frame_rate(self.target_sample_rate)
            
            # Check duration and truncate if necessary
            duration_ms = len(audio)
            max_duration_ms = self.max_duration * 1000
            if duration_ms > max_duration_ms:
                logger.warning(f"Truncating audio from {duration_ms/1000:.1f}s to {self.max_duration}s")
                audio = audio[:max_duration_ms]
            
            # Normalize volume
            audio = audio.normalize()
            
            # Export as WAV
            audio.export(output_path, format="wav")
            
            # Verify output file
            if not os.path.exists(output_path):
                raise RuntimeError("Failed to create output file with pydub")
            
            logger.debug(f"Pydub conversion successful: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Fallback conversion failed: {e}")
            # Last resort: return original file
            logger.warning("Using original file without processing")
            return input_path
    
    def get_audio_info(self, file_path: str) -> dict:
        """
        Get information about an audio file.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Dictionary with audio information
        """
        try:
            # Try librosa first
            audio, sr = librosa.load(file_path, sr=None)
            duration = len(audio) / sr
            
            return {
                "duration": duration,
                "sample_rate": sr,
                "channels": 1 if len(audio.shape) == 1 else audio.shape[1],
                "samples": len(audio),
                "format": "detected by librosa"
            }
            
        except Exception:
            # Fallback to pydub
            try:
                audio = AudioSegment.from_file(file_path)
                return {
                    "duration": len(audio) / 1000.0,  # Convert ms to seconds
                    "sample_rate": audio.frame_rate,
                    "channels": audio.channels,
                    "samples": len(audio.raw_data),
                    "format": "detected by pydub"
                }
            except Exception as e:
                logger.error(f"Failed to get audio info: {e}")
                return {
                    "duration": 0,
                    "sample_rate": 0,
                    "channels": 0,
                    "samples": 0,
                    "format": "unknown",
                    "error": str(e)
                }
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate that the file is a proper audio file.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            True if valid audio file, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False
            
            # Check file size
            if os.path.getsize(file_path) == 0:
                return False
            
            # Try to load with librosa
            try:
                audio, sr = librosa.load(file_path, duration=1.0)  # Load just 1 second
                return len(audio) > 0 and sr > 0
            except Exception:
                # Try with pydub
                try:
                    audio = AudioSegment.from_file(file_path)
                    return len(audio) > 0
                except Exception:
                    return False
                    
        except Exception:
            return False
    
    def cleanup_temp_files(self, file_path: str) -> None:
        """
        Clean up temporary audio files.
        
        Args:
            file_path: Path to file/directory to clean up
        """
        try:
            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.debug(f"Cleaned up temp file: {file_path}")
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                    logger.debug(f"Cleaned up temp directory: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup {file_path}: {e}")
    
    async def estimate_processing_time(self, file_path: str) -> float:
        """
        Estimate processing time for an audio file.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Estimated processing time in seconds
        """
        try:
            info = self.get_audio_info(file_path)
            duration = info.get("duration", 0)
            
            # Rough estimates based on file duration
            if duration == 0:
                return 5.0  # Default for unknown
            elif duration <= 60:  # 1 minute
                return 10.0
            elif duration <= 300:  # 5 minutes
                return 30.0
            elif duration <= 600:  # 10 minutes
                return 60.0
            else:
                return 120.0  # Longer files
                
        except Exception:
            return 30.0  # Default estimate