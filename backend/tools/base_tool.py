from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class ToolResult(BaseModel):
    """Result from a tool execution"""
    success: bool
    result: Any
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseTool(ABC):
    """Abstract base class for all agent tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass
    
    def get_info(self) -> Dict[str, str]:
        """Get tool information"""
        return {
            "name": self.name,
            "description": self.description
        } 