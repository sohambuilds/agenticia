import re
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from .math_agent import MathAgent
from .physics_agent import PhysicsAgent
from models import AgentRequest, AgentResponse, AgentType
import logging

logger = logging.getLogger(__name__)

class TutorAgent(BaseAgent):
    """Main orchestrator agent that delegates queries to specialized agents"""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.TUTOR,
            description="Main tutoring agent that coordinates with specialized math and physics agents to provide comprehensive educational support"
        )
        
        # Initialize specialized agents
        self.math_agent = MathAgent()
        self.physics_agent = PhysicsAgent()
        
        # Classification keywords for routing
        self.math_keywords = [
            # Basic math
            "calculate", "compute", "solve", "evaluate", "math", "mathematics",
            "algebra", "geometry", "calculus", "trigonometry", "statistics",
            "equation", "function", "derivative", "integral", "polynomial",
            "+", "-", "*", "/", "×", "÷", "^", "**", "=", "equals",
            "sqrt", "sin", "cos", "tan", "log", "ln", "abs", "round",
            
            # Mathematical concepts
            "theorem", "proof", "formula", "matrix", "vector", "probability",
            "graph", "plot", "linear", "quadratic", "exponential"
        ]
        
        self.physics_keywords = [
            # General physics
            "physics", "force", "energy", "motion", "velocity", "acceleration",
            "momentum", "gravity", "mass", "weight", "pressure", "volume",
            
            # Mechanics
            "newton", "kinetic", "potential", "friction", "displacement",
            
            # Thermodynamics
            "temperature", "heat", "thermal", "gas", "entropy", "enthalpy",
            
            # Electromagnetism
            "electric", "magnetic", "current", "voltage", "resistance",
            "charge", "field", "electromagnetic",
            
            # Waves and modern physics
            "wave", "frequency", "wavelength", "light", "quantum", "relativity",
            "photon", "electron", "proton", "neutron", "atomic", "nuclear",
            
            # Units and constants
            "joule", "watt", "newton", "meter", "kilogram", "second", "ampere",
            "coulomb", "volt", "ohm", "hertz"
        ]
        
        # General educational keywords
        self.general_education_keywords = [
            "explain", "what is", "how does", "why", "definition", "concept",
            "example", "help", "understand", "learn", "study", "homework",
            "assignment", "question", "problem", "exercise"
        ]
    
    async def _process_specialized_query(self, request: AgentRequest) -> Dict[str, Any]:
        """Route queries to appropriate specialized agents or handle general tutoring"""
        query = request.query
        
        # Determine which agent should handle the query
        agent_choice = self._classify_query(query)
        
        logger.info(f"Tutor agent routing query to: {agent_choice}")
        
        # Delegate to specialized agent or handle directly
        if agent_choice == AgentType.MATH:
            response = await self.math_agent.process_query(request)
            return self._wrap_delegated_response(response, "math")
            
        elif agent_choice == AgentType.PHYSICS:
            response = await self.physics_agent.process_query(request)
            return self._wrap_delegated_response(response, "physics")
            
        else:
            # Handle as general tutoring query
            return await self._handle_general_tutoring(request)
    
    def _classify_query(self, query: str) -> AgentType:
        """Classify query to determine which agent should handle it"""
        query_lower = query.lower()
        
        # Count keyword matches for each domain
        math_score = sum(1 for keyword in self.math_keywords if keyword in query_lower)
        physics_score = sum(1 for keyword in self.physics_keywords if keyword in query_lower)
        
        # Bonus scoring for explicit domain mentions
        if "math" in query_lower or "mathematics" in query_lower:
            math_score += 3
        if "physics" in query_lower or "physical" in query_lower:
            physics_score += 3
        
        # Advanced pattern matching for specific problem types
        math_score += self._detect_math_patterns(query)
        physics_score += self._detect_physics_patterns(query)
        
        logger.info(f"Classification scores - Math: {math_score}, Physics: {physics_score}")
        
        # Decision logic
        if math_score > physics_score and math_score >= 2:
            return AgentType.MATH
        elif physics_score > math_score and physics_score >= 2:
            return AgentType.PHYSICS
        elif math_score == physics_score and math_score >= 2:
            # Use additional context to break ties
            return self._resolve_tie(query_lower)
        else:
            # Default to tutor for general queries
            return AgentType.TUTOR
    
    def _detect_math_patterns(self, query: str) -> int:
        """Detect mathematical patterns in the query"""
        score = 0
        
        # Mathematical expressions
        if re.search(r'\d+\s*[+\-*/^]\s*\d+', query):
            score += 2
        
        # Function notation
        if re.search(r'f\(x\)|g\(x\)|h\(x\)', query):
            score += 2
            
        # Mathematical symbols and notation
        if re.search(r'[∫∑∆αβγθπ]', query):
            score += 3
            
        # Equation patterns
        if re.search(r'=.*[x-z]|[x-z].*=', query):
            score += 2
        
        return score
    
    def _detect_physics_patterns(self, query: str) -> int:
        """Detect physics patterns in the query"""
        score = 0
        
        # Physics formulas (F=ma, E=mc^2, etc.)
        if re.search(r'F\s*=\s*m.*a|E\s*=\s*m.*c|P\s*=\s*F/A', query, re.IGNORECASE):
            score += 3
            
        # Units pattern
        if re.search(r'\d+\s*(m/s|kg|N|J|W|V|A|Ω|Hz)', query):
            score += 2
            
        # Physics constants
        if re.search(r'\b(9\.8|3\.0.*10\^8|6\.67.*10\^-11)\b', query):
            score += 2
            
        # Physics problem keywords
        if re.search(r'object.*moving|ball.*thrown|car.*travels|spring.*compressed', query, re.IGNORECASE):
            score += 2
        
        return score
    
    def _resolve_tie(self, query_lower: str) -> AgentType:
        """Resolve ties between math and physics classification"""
        # Look for context clues
        if any(word in query_lower for word in ["real world", "application", "experiment"]):
            return AgentType.PHYSICS
        elif any(word in query_lower for word in ["abstract", "theoretical", "pure"]):
            return AgentType.MATH
        else:
            # Default to math for mathematical expressions
            if re.search(r'\d+\s*[+\-*/^]\s*\d+', query_lower):
                return AgentType.MATH
            else:
                return AgentType.TUTOR
    
    async def _handle_general_tutoring(self, request: AgentRequest) -> Dict[str, Any]:
        """Handle general tutoring queries that don't require specialized agents"""
        query = request.query
        
        # Build general tutoring system prompt
        system_prompt = """You are an AI Tutor Agent specializing in educational support. Your role is to:

1. Provide clear, helpful explanations on academic topics
2. Guide students through learning concepts step by step
3. Encourage critical thinking and problem-solving
4. Adapt explanations to different learning levels
5. Suggest additional resources when appropriate

Guidelines:
- Use encouraging, supportive language
- Break complex topics into manageable parts
- Provide examples to illustrate concepts
- Ask clarifying questions when needed
- Connect learning to real-world applications
- If the question is specifically about math or physics calculations, suggest that the student ask more specifically about those topics for detailed assistance

For questions that require detailed mathematical calculations or physics problem-solving, you can suggest that students specify they need "math help" or "physics help" for more specialized assistance."""

        # Generate response
        ai_response = await self._call_gemini_api(query, system_prompt)
        
        return {
            "text": ai_response,
            "tools_used": [],
            "confidence": 0.75,
            "metadata": {
                "handled_by": "general_tutor",
                "query_classification": "general",
                "suggestion": "For specific math or physics calculations, try asking with 'math:' or 'physics:' prefix"
            }
        }
    
    def _wrap_delegated_response(self, agent_response: AgentResponse, agent_type: str) -> Dict[str, Any]:
        """Wrap response from delegated agent"""
        return {
            "text": agent_response.response,
            "tools_used": agent_response.tools_used or [],
            "confidence": agent_response.confidence or 0.8,
            "metadata": {
                "delegated_to": agent_type,
                "original_agent_type": agent_response.agent_type,
                "original_metadata": agent_response.metadata
            }
        }
    
    def get_routing_info(self) -> Dict[str, Any]:
        """Get information about query routing capabilities"""
        return {
            "available_agents": {
                "math": self.math_agent.get_agent_info(),
                "physics": self.physics_agent.get_agent_info()
            },
            "classification_keywords": {
                "math": self.math_keywords[:10],  # Show first 10 for brevity
                "physics": self.physics_keywords[:10]
            },
            "routing_logic": {
                "method": "keyword_scoring_with_pattern_detection",
                "tie_resolution": "context_clues_and_expression_analysis",
                "minimum_score": 2
            }
        } 