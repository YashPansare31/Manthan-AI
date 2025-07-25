from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Speaker(BaseModel):
    id: str
    name: Optional[str] = None
    segments: List[Dict[str, Any]] = []

class ActionItem(BaseModel):
    text: str
    assignee: Optional[str] = None
    deadline: Optional[str] = None
    priority: str = "medium"
    confidence: float = 0.0

class Decision(BaseModel):
    text: str
    context: str
    participants: List[str] = []
    confidence: float = 0.0

class AnalysisResponse(BaseModel):
    transcript: str
    speakers: List[Speaker] = []
    action_items: List[ActionItem] = []
    decisions: List[Decision] = []
    key_topics: List[str] = []
    sentiment_analysis: Dict[str, Any] = {}
    summary: str
    confidence_score: float
    processing_time: float
    timestamp: datetime = datetime.now()