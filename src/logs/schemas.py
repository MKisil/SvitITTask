from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class SearchParams(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    keyword: Optional[str] = None
    level: Optional[str] = None


class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str
    user_id: int


class SearchResponse(BaseModel):
    total: int
    logs: List[LogEntry]
