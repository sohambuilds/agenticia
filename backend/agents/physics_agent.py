import re
from typing import Dict, Any, List
from .base_agent import BaseAgent
from models import AgentRequest, AgentType
from tools import PhysicsConstantsTool, CalculatorTool
import logging

logger = logging.getLogger(__name__)

class PhysicsAgent(BaseAgent):
    """Specialized agent for physics problems and concepts"""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.PHYSICS,
            description="Specialized in physics problems, formulas, constants, and concepts including mechanics, thermodynamics, electromagnetism, and quantum physics"
        )
        
        # Add physics and calculation tools
        self.add_tool(PhysicsConstantsTool())
        self.add_tool(CalculatorTool())
        
        # Physics concepts and keywords
        self.physics_concepts = [
            # Mechanics
            "force", "velocity", "acceleration", "momentum", "energy", "kinetic", "potential",
            "friction", "gravity", "mass", "weight", "newton", "motion", "displacement",
            
            # Thermodynamics
            "temperature", "heat", "entropy", "enthalpy", "thermal", "gas", "pressure",
            "volume", "ideal gas", "carnot", "thermodynamic",
            
            # Electromagnetism
            "electric", "magnetic", "current", "voltage", "resistance", "capacitance",
            "inductance", "electromagnetic", "field", "charge", "coulomb", "ampere",
            "ohm", "faraday", "maxwell",
            
            # Waves and Optics
            "wave", "frequency", "wavelength", "amplitude", "light", "optics", "reflection",
            "refraction", "interference", "diffraction", "polarization",
            
            # Modern Physics
            "quantum", "relativity", "photon", "electron", "proton", "neutron", "atomic",
            "nuclear", "radioactive", "planck", "einstein", "bohr"
        ]
        
        # Constants that are commonly referenced
        self.common_constants = [
            "c", "h", "hbar", "e", "me", "mp", "mn", "G", "k", "NA", "R",
            "eps0", "mu0", "ke", "g", "atm", "sigma", "pi", "euler"
        ]
        
        # Formula keywords for common physics formulas
        self.formula_keywords = {
            "kinetic_energy": ["kinetic energy", "ke", "1/2 mv"],
            "potential_energy": ["potential energy", "pe", "mgh"],
            "force": ["newton's law", "f=ma", "force"],
            "gravitational_force": ["gravity", "gravitational force", "newton's gravity"],
            "coulomb_law": ["coulomb", "electrostatic", "electric force"],
            "ohms_law": ["ohm", "v=ir", "resistance"],
            "wave_equation": ["wave", "velocity", "frequency", "wavelength"],
            "ideal_gas": ["ideal gas", "pv=nrt", "gas law"]
        }
    
    async def _process_specialized_query(self, request: AgentRequest) -> Dict[str, Any]:
        """Process physics queries with constants and formula lookup"""
        query = request.query
        tools_used = []
        confidence = 0.85  # Default confidence for physics agent
        
        # Detect physics constants needed
        constants_found = await self._find_and_lookup_constants(query)
        if constants_found["constants"]:
            tools_used.append("physics_constants")
        
        # Detect formulas needed
        formulas_found = await self._find_and_lookup_formulas(query)
        if formulas_found["formulas"]:
            tools_used.append("physics_constants")
        
        # Extract and perform calculations if needed
        calculations_needed = self._extract_physics_calculations(query)
        calculation_results = {}
        
        if calculations_needed:
            for calc in calculations_needed:
                calc_result = await self._use_tool("calculator", calc)
                tools_used.append("calculator")
                
                if calc_result.success:
                    calculation_results[calc] = calc_result.result
                    logger.info(f"Physics calculation: {calc} = {calc_result.result}")
        
        # Build comprehensive system prompt
        system_prompt = self._build_physics_system_prompt(
            constants_found, formulas_found, calculation_results
        )
        
        # Get AI response with physics context
        ai_response = await self._call_gemini_api(query, system_prompt)
        
        # Enhance response with physics data
        ai_response = self._enhance_physics_response(
            ai_response, constants_found, formulas_found, calculation_results
        )
        
        return {
            "text": ai_response,
            "tools_used": list(set(tools_used)),
            "confidence": confidence,
            "metadata": {
                "physics_concepts_detected": self._detect_physics_concepts(query),
                "constants_used": list(constants_found["constants"].keys()),
                "formulas_used": list(formulas_found["formulas"].keys()),
                "calculations_performed": len(calculation_results),
                "calculation_results": calculation_results
            }
        }
    
    async def _find_and_lookup_constants(self, query: str) -> Dict[str, Any]:
        """Find and look up physics constants mentioned in the query"""
        found_constants = {}
        query_lower = query.lower()
        
        # Look for explicit constant symbols
        for constant in self.common_constants:
            if f" {constant} " in f" {query_lower} " or f"={constant}" in query_lower:
                result = await self._use_tool("physics_constants", constant, query_type="constant")
                if result.success:
                    found_constants[constant] = result.result
        
        # Look for constant descriptions
        constant_patterns = {
            "speed of light": "c",
            "planck constant": "h",
            "elementary charge": "e",
            "electron mass": "me",
            "gravitational constant": "g",
            "boltzmann constant": "k",
            "avogadro": "NA",
            "gas constant": "R"
        }
        
        for description, symbol in constant_patterns.items():
            if description in query_lower:
                result = await self._use_tool("physics_constants", symbol, query_type="constant")
                if result.success:
                    found_constants[symbol] = result.result
        
        return {"constants": found_constants}
    
    async def _find_and_lookup_formulas(self, query: str) -> Dict[str, Any]:
        """Find and look up physics formulas mentioned in the query"""
        found_formulas = {}
        query_lower = query.lower()
        
        # Check for formula keywords
        for formula_name, keywords in self.formula_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    result = await self._use_tool("physics_constants", formula_name, query_type="formula")
                    if result.success:
                        found_formulas[formula_name] = result.result
                    break  # Only add formula once
        
        return {"formulas": found_formulas}
    
    def _extract_physics_calculations(self, query: str) -> List[str]:
        """Extract physics calculations from the query"""
        calculations = []
        
        # Physics-specific calculation patterns
        patterns = [
            # Force calculations: F = ma, F = 5 * 2
            r'F\s*=\s*[0-9+\-*/().\s]+',
            
            # Energy calculations: KE = 1/2 * m * v^2
            r'(?:KE|PE)\s*=\s*[0-9+\-*/().\s^]+',
            
            # Basic arithmetic with units (extract just the numbers)
            r'\b\d+(?:\.\d+)?\s*[+\-*/^]\s*\d+(?:\.\d+)?(?:\s*[+\-*/^]\s*\d+(?:\.\d+)?)*',
            
            # Function calls in physics context
            r'\b(?:sin|cos|tan|sqrt|log|abs)\s*\(\s*[0-9+\-*/^().\s]+\s*\)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                # Clean the match - remove variable names and keep only numbers/operators
                cleaned = re.sub(r'[A-Za-z]', '', match)  # Remove letters
                cleaned = re.sub(r'=+', '', cleaned)      # Remove equals signs
                cleaned = cleaned.strip()
                
                if cleaned and self._is_valid_physics_calculation(cleaned):
                    calculations.append(cleaned)
        
        return calculations
    
    def _is_valid_physics_calculation(self, expression: str) -> bool:
        """Check if expression is a valid physics calculation"""
        # Must contain numbers and operators, no alphabetic characters
        has_number = re.search(r'\d', expression)
        has_operator = re.search(r'[+\-*/^]', expression)
        no_letters = not re.search(r'[A-Za-z]', expression)
        
        return has_number and has_operator and no_letters and len(expression.strip()) > 2
    
    def _detect_physics_concepts(self, query: str) -> List[str]:
        """Detect physics concepts mentioned in the query"""
        detected = []
        query_lower = query.lower()
        
        for concept in self.physics_concepts:
            if concept in query_lower:
                detected.append(concept)
        
        return detected
    
    def _build_physics_system_prompt(self, constants_data: Dict, formulas_data: Dict, calculations: Dict) -> str:
        """Build comprehensive system prompt for physics context"""
        base_prompt = """You are a specialized Physics Tutor Agent. Your role is to:

1. Solve physics problems step by step
2. Explain physics concepts clearly with real-world applications
3. Use appropriate physics formulas and constants
4. Show detailed calculations and unit analysis
5. Help students understand the underlying physics principles

Guidelines:
- Always include units in your calculations
- Explain the physics concepts behind each step
- Reference relevant formulas and constants when applicable
- Show dimensional analysis when helpful
- Connect problems to real-world physics applications
- Use clear, educational language suitable for students"""

        # Add constants context
        if constants_data["constants"]:
            const_context = "\n\nPhysics Constants Available:\n"
            for symbol, data in constants_data["constants"].items():
                const_context += f"- {symbol}: {data['value']} {data['unit']} ({data['description']})\n"
            base_prompt += const_context
        
        # Add formulas context
        if formulas_data["formulas"]:
            formula_context = "\n\nRelevant Physics Formulas:\n"
            for name, data in formulas_data["formulas"].items():
                formula_context += f"- {name.replace('_', ' ').title()}: {data['formula']}\n"
                formula_context += f"  Description: {data['description']}\n"
            base_prompt += formula_context
        
        # Add calculation context
        if calculations:
            calc_context = "\n\nCalculation Results Available:\n"
            for expr, result in calculations.items():
                calc_context += f"- {expr} = {result}\n"
            calc_context += "\nUse these results in your physics explanation."
            base_prompt += calc_context
        
        return base_prompt
    
    def _enhance_physics_response(self, response: str, constants_data: Dict, 
                                formulas_data: Dict, calculations: Dict) -> str:
        """Enhance response with physics data if not already included"""
        
        # Add constants section if used but not mentioned
        if constants_data["constants"] and "constant" not in response.lower():
            const_section = "\n\n**Physics Constants Used:**\n"
            for symbol, data in constants_data["constants"].items():
                const_section += f"- {symbol} = {data['value']} {data['unit']} ({data['description']})\n"
            response += const_section
        
        # Add formulas section if used but not mentioned
        if formulas_data["formulas"] and "formula" not in response.lower():
            formula_section = "\n\n**Relevant Formulas:**\n"
            for name, data in formulas_data["formulas"].items():
                formula_section += f"- {data['formula']} - {data['description']}\n"
            response += formula_section
        
        # Add calculations if performed
        if calculations and "calculation" not in response.lower():
            calc_section = "\n\n**Calculations:**\n"
            for expr, result in calculations.items():
                calc_section += f"- {expr} = {result}\n"
            response += calc_section
        
        return response 