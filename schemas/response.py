from pydantic import BaseModel
from typing import Optional, Dict

class ResponsePayload(BaseModel):
    tool_name: str
    success: bool
    output: Optional[Dict] = None  # raw tool output
    human_readable: Optional[str] = None  # optional summary for chatbots
    timestamp: Optional[str] = None  # ISO 8601 timestamp
    error: Optional[str] = None

