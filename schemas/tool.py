from pydantic import BaseModel
from typing import Optional, Dict

class ToolContext(BaseModel):
    tool_name: str  # e.g., "wayback_machine"
    version: Optional[str] = "v1"
    goal: Optional[str] = None  # e.g., "retrieve 2011 jQuery plugin page"
    inputs: Dict[str, str]  # tool-specific inputs
    fallback_strategy: Optional[str] = "try_closest_match"
    priority: Optional[int] = 1

