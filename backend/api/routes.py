from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse, HealthResponse, AgentType
import uuid

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - will be implemented in Phase 4
    For now, returns a placeholder response
    """

    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    return ChatResponse(
        response="Hello! I'm your AI tutor. I'll be fully functional soon!",
        agent_used=AgentType.TUTOR,
        conversation_id=conversation_id,
        metadata={"status": "placeholder"}
    )

@router.get("/agents", response_model=list[str])
async def list_agents():
    """
    List available agents
    """
    return ["tutor", "math", "physics"]

@router.get("/health", response_model=HealthResponse)
async def detailed_health_check():
    """
    Detailed health check with agent status
    """
    return HealthResponse(
        status="healthy",
        service="ai-tutor-backend",
        agents_available=["tutor", "math", "physics"]
    ) 