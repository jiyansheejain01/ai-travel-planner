from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MemoryRecord(BaseModel):
    user_id: str
    memory_type: str  # preference, feedback, trip_history
    text: str
    created_at: datetime
    importance: float = 0.5


class RetrievedMemory(BaseModel):
    text: str
    memory_type: str
    score: float