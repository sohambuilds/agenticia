import re
from typing import Dict, Any, List
from .base_agent import BaseAgent
from models import AgentRequest, AgentType
from tools import CalculatorTool
import logging

logger = logging.getLogger(__name__)

class MathAgent(BaseAgent):
   #AGENT FOR MATH PROBLEMS
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.MATH,
            description="Specialized in solving mathematical problems, performing calculations, and explaining mathematical concepts"
        )
        
        # Add calculator tool
        self.add_tool(CalculatorTool())
        
        # Keywords that indicate calculator usage
        self.calculator_keywords = [
            "calculate", "compute", "solve", "evaluate", "find the value",
            "+", "-", "*", "/", "×", "÷", "^", "**", "sqrt", "sin", "cos", "tan",
            "log", "ln", "abs", "round", "ceil", "floor", "=", "equals"
        ]
        
        # Mathematical concepts keywords
        self.math_concepts = [
            "algebra", "geometry", "calculus", "trigonometry", "statistics",
            "probability", "equation", "function", "derivative", "integral",
            "matrix", "vector", "polynomial", "theorem", "proof", "formula"
        ]
    
    async def _process_specialized_query(self, request: AgentRequest) -> Dict[str, Any]:
        """Process mathematical queries with calculation support"""
        query = request.query
        tools_used = []
        confidence = 0.8  # Default confidence for math agent
        
        # Check if we need to use calculator
        calculations_needed = self._extract_calculations(query)
        calculation_results = {}
        
        if calculations_needed:
            logger.info(f"Found {len(calculations_needed)} calculations to perform")
            for i, calc in enumerate(calculations_needed):
                calc_result = await self._use_tool("calculator", calc)
                tools_used.append("calculator")
                
                if calc_result.success:
                    calculation_results[calc] = calc_result.result
                    logger.info(f"Calculated {calc} = {calc_result.result}")
                else:
                    logger.warning(f"Calculation failed for {calc}: {calc_result.error_message}")
                    calculation_results[calc] = f"Error: {calc_result.error_message}"
        
        # Generate system prompt for math context
        system_prompt = self._build_math_system_prompt(calculation_results)
        
        # Get AI response with calculation context
        ai_response = await self._call_gemini_api(query, system_prompt)
        
        # If we performed calculations, include them in the response
        if calculation_results:
            ai_response = self._enhance_response_with_calculations(ai_response, calculation_results)
        
        return {
            "text": ai_response,
            "tools_used": list(set(tools_used)),  # Remove duplicates
            "confidence": confidence,
            "metadata": {
                "calculations_performed": len(calculation_results),
                "calculation_results": calculation_results,
                "math_concepts_detected": self._detect_math_concepts(query)
            }
        }
    
    def _extract_calculations(self, query: str) -> List[str]:
        """Extract mathematical expressions that need calculation"""
        calculations = []
        
        # Pattern for mathematical expressions
        # Matches expressions like: 2+3, 5*7, sqrt(16), sin(30), etc.
        patterns = [
            # Basic arithmetic: numbers with operators
            r'\b\d+(?:\.\d+)?\s*[+\-*/^]\s*\d+(?:\.\d+)?(?:\s*[+\-*/^]\s*\d+(?:\.\d+)?)*',
            
            # Function calls: sin(30), sqrt(16), log(10), etc.
            r'\b(?:sin|cos|tan|sqrt|log|log10|abs|ceil|floor|round)\s*\(\s*[0-9+\-*/^().\s]+\s*\)',
            
            # Expressions with parentheses
            r'\([0-9+\-*/^().\s]+\)',
            
            # Power notation: 2^3, 5**2
            r'\b\d+(?:\.\d+)?\s*[\^*]{1,2}\s*\d+(?:\.\d+)?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query)
            for match in matches:
                # Clean up the match
                cleaned = match.strip()
                if cleaned and self._is_valid_calculation(cleaned):
                    calculations.append(cleaned)
        
        # Also look for explicit calculation requests
        calc_patterns = [
            r'calculate\s+([0-9+\-*/^().\s]+)',
            r'compute\s+([0-9+\-*/^().\s]+)',
            r'evaluate\s+([0-9+\-*/^().\s]+)',
            r'solve\s+([0-9+\-*/^().\s=]+)',
        ]
        
        for pattern in calc_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                cleaned = match.replace('=', '').strip()
                if cleaned and self._is_valid_calculation(cleaned):
                    calculations.append(cleaned)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_calculations = []
        for calc in calculations:
            if calc not in seen:
                seen.add(calc)
                unique_calculations.append(calc)
        
        return unique_calculations
    
    def _is_valid_calculation(self, expression: str) -> bool:
        """Check if an expression is a valid calculation"""
        # Must contain at least one number and one operator or function
        has_number = re.search(r'\d', expression)
        has_operator = re.search(r'[+\-*/^]', expression)
        has_function = re.search(r'\b(?:sin|cos|tan|sqrt|log|abs|ceil|floor|round)\b', expression)
        
        return has_number and (has_operator or has_function)
    
    def _detect_math_concepts(self, query: str) -> List[str]:
        """Detect mathematical concepts mentioned in the query"""
        detected = []
        query_lower = query.lower()
        
        for concept in self.math_concepts:
            if concept in query_lower:
                detected.append(concept)
        
        return detected
    
    def _build_math_system_prompt(self, calculation_results: Dict[str, Any]) -> str:
        """Build system prompt for mathematical context"""
        base_prompt = """You are a specialized Math Tutor Agent. Your role is to:

1. Solve mathematical problems step by step
2. Explain mathematical concepts clearly
3. Provide detailed working and reasoning
4. Use calculation results when available
5. Help students understand the underlying principles

Guidelines:
- Always show your working step by step
- Explain the mathematical reasoning behind each step
- Use simple language while maintaining mathematical accuracy
- If calculations were performed, reference them appropriately
- Include formulas and theorems when relevant"""

        if calculation_results:
            calc_context = "\n\nCalculation Results Available:\n"
            for expr, result in calculation_results.items():
                calc_context += f"- {expr} = {result}\n"
            calc_context += "\nUse these results in your explanation when appropriate."
            base_prompt += calc_context
        
        return base_prompt
    
    def _enhance_response_with_calculations(self, response: str, calculations: Dict[str, Any]) -> str:
        """Enhance the AI response with calculation results"""
        if not calculations:
            return response
        
        # Add a calculations section if not already included
        if "calculation" not in response.lower():
            calc_section = "\n\n**Calculations:**\n"
            for expr, result in calculations.items():
                calc_section += f"- {expr} = {result}\n"
            response += calc_section
        
        return response 