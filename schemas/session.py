from pydantic import BaseModel
from typing import List, Optional
from .tool import ToolContext
from .response import ResponsePayload

class SessionContext(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    task_description: str
    conversation_history: Optional[List[str]] = []
    current_step: Optional[str] = None  # e.g. "fetching data", "summarizing", etc.
    tools_invoked: List[ToolContext]
    results: Optional[List[ResponsePayload]] = []

