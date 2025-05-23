from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import google.generativeai as genai
from models import AgentRequest, AgentResponse, AgentType
from tools import BaseTool, ToolResult
from config import settings
import logging
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for all AI agents"""
    
    def __init__(self, agent_type: AgentType, description: str):
        self.agent_type = agent_type
        self.description = description
        self.tools: Dict[str, BaseTool] = {}
        
        # Configure Gemini API
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            logger.warning("Gemini API key not found. Agent will operate in mock mode.")
            self.model = None
    
    def add_tool(self, tool: BaseTool) -> None:
        """Add a tool to this agent"""
        self.tools[tool.name] = tool
        logger.info(f"Added tool '{tool.name}' to {self.agent_type} agent")
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return list(self.tools.keys())
    
    async def process_query(self, request: AgentRequest) -> AgentResponse:
        """
        Process a query using this agent
        
        Args:
            request: AgentRequest containing the query and context
            
        Returns:
            AgentResponse with the agent's response
        """
        try:
            logger.info(f"{self.agent_type} agent processing query: {request.query[:100]}...")
            
            # Let specialized agents implement their own logic
            response = await self._process_specialized_query(request)
            
            return AgentResponse(
                response=response["text"],
                agent_type=self.agent_type,
                tools_used=response.get("tools_used", []),
                confidence=response.get("confidence"),
                metadata=response.get("metadata", {})
            )
            
        except Exception as e:
            logger.error(f"Error in {self.agent_type} agent: {str(e)}")
            return AgentResponse(
                response=f"I apologize, but I encountered an error while processing your request: {str(e)}",
                agent_type=self.agent_type,
                tools_used=[],
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    @abstractmethod
    async def _process_specialized_query(self, request: AgentRequest) -> Dict[str, Any]:
        """
        Specialized query processing logic implemented by each agent
        
        Args:
            request: AgentRequest containing the query and context
            
        Returns:
            Dict with response text, tools_used, confidence, and metadata
        """
        pass
    
    async def _call_gemini_api(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Call Gemini API with error handling and retries
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Generated response text
        """
        if not self.model:
            return "I'm currently unable to process requests due to API configuration issues."
        
        try:
            # Combine system prompt and user prompt if system prompt is provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser Query: {prompt}"
            
            # Generate response with configured parameters
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=settings.max_response_tokens,
                    temperature=settings.temperature,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise Exception(f"AI service error: {str(e)}")
    
    async def _use_tool(self, tool_name: str, *args, **kwargs) -> ToolResult:
        """
        Use a specific tool
        
        Args:
            tool_name: Name of the tool to use
            *args, **kwargs: Arguments to pass to the tool
            
        Returns:
            ToolResult from the tool execution
        """
        if tool_name not in self.tools:
            return ToolResult(
                success=False,
                result=None,
                error_message=f"Tool '{tool_name}' not available"
            )
        
        try:
            logger.info(f"Using tool: {tool_name}")
            result = await self.tools[tool_name].execute(*args, **kwargs)
            logger.info(f"Tool {tool_name} result: success={result.success}")
            return result
        except Exception as e:
            logger.error(f"Tool {tool_name} error: {str(e)}")
            return ToolResult(
                success=False,
                result=None,
                error_message=f"Tool execution error: {str(e)}"
            )
    
    def _should_use_tool(self, query: str, tool_keywords: List[str]) -> bool:
        """
        Determine if a tool should be used based on query content
        
        Args:
            query: User query
            tool_keywords: Keywords that indicate tool usage
            
        Returns:
            True if tool should be used
        """
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in tool_keywords)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent"""
        return {
            "type": self.agent_type,
            "description": self.description,
            "available_tools": self.get_available_tools(),
            "tool_descriptions": {name: tool.description for name, tool in self.tools.items()}
        } 