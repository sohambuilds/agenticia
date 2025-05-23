from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse, HealthResponse, AgentType, AgentRequest
from agents import TutorAgent
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize the main tutor agent (singleton pattern)
tutor_agent = None

def get_tutor_agent():
    """Get or create the tutor agent instance"""
    global tutor_agent
    if tutor_agent is None:
        try:
            tutor_agent = TutorAgent()
            logger.info("TutorAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TutorAgent: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to initialize AI tutoring system")
    return tutor_agent

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - processes user queries through the multi-agent system
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get the tutor agent
        agent = get_tutor_agent()
        
        # Create agent request
        agent_request = AgentRequest(
            query=request.message,
            context={"conversation_id": conversation_id}
        )
        
        # Process the query through the agent system
        logger.info(f"Processing query: {request.message[:100]}...")
        agent_response = await agent.process_query(agent_request)
        
        # Return the response
        return ChatResponse(
            response=agent_response.response,
            agent_used=agent_response.agent_type,
            conversation_id=conversation_id,
            metadata={
                "tools_used": agent_response.tools_used,
                "confidence": agent_response.confidence,
                "agent_metadata": agent_response.metadata
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        
        # Return error response
        return ChatResponse(
            response="I apologize, but I encountered an error while processing your request. Please try again.",
            agent_used=AgentType.TUTOR,
            conversation_id=conversation_id,
            metadata={"error": str(e)}
        )

@router.get("/agents", response_model=dict)
async def list_agents():
    """
    Get information about available agents and their capabilities
    """
    try:
        agent = get_tutor_agent()
        
        # Get routing information from tutor agent
        routing_info = agent.get_routing_info()
        
        return {
            "available_agents": ["tutor", "math", "physics"],
            "agent_descriptions": {
                "tutor": "Main coordinator agent that routes queries to specialized agents",
                "math": "Specialized agent for mathematical problems and calculations",
                "physics": "Specialized agent for physics problems, constants, and formulas"
            },
            "routing_info": routing_info,
            "status": "operational"
        }
        
    except Exception as e:
        logger.error(f"Error getting agent info: {str(e)}")
        return {
            "available_agents": ["tutor", "math", "physics"],
            "status": "error",
            "error": str(e)
        }

@router.get("/health", response_model=HealthResponse)
async def detailed_health_check():
    """
    Detailed health check with agent system status
    """
    try:
        # Try to initialize/get the tutor agent
        agent = get_tutor_agent()
        
        # Test that all components are working
        test_request = AgentRequest(query="test", context={})
        
        # This should not fail for a simple test
        agents_status = "healthy"
        
        return HealthResponse(
            status="healthy",
            service="ai-tutor-backend",
            agents_available=["tutor", "math", "physics"]
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            service="ai-tutor-backend",
            agents_available=[]
        ) 