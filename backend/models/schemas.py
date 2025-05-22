from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

class AgentType(str, Enum):
    TUTOR = "tutor"
    MATH = "math"
    PHYSICS = "physics"

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    agent_used: AgentType
    conversation_id: str
    metadata: Optional[Dict[str, Any]] = None

class AgentRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    response: str
    agent_type: AgentType
    tools_used: Optional[list[str]] = None
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    agents_available: list[str] 