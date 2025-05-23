from typing import Dict, List, Optional
from .base_tool import BaseTool, ToolResult

class PhysicsConstantsTool(BaseTool):
    """Tool for looking up physics constants and formulas"""
    
    def __init__(self):
        super().__init__(
            name="physics_constants",
            description="Provides access to fundamental physics constants, common formulas, and unit conversions"
        )
        
        # Fundamental physics constants
        self.constants = {
            # Fundamental constants
            "c": {"value": 299792458, "unit": "m/s", "description": "Speed of light in vacuum"},
            "h": {"value": 6.62607015e-34, "unit": "J⋅s", "description": "Planck constant"},
            "hbar": {"value": 1.054571817e-34, "unit": "J⋅s", "description": "Reduced Planck constant"},
            "e": {"value": 1.602176634e-19, "unit": "C", "description": "Elementary charge"},
            "me": {"value": 9.1093837015e-31, "unit": "kg", "description": "Electron mass"},
            "mp": {"value": 1.67262192369e-27, "unit": "kg", "description": "Proton mass"},
            "mn": {"value": 1.67492749804e-27, "unit": "kg", "description": "Neutron mass"},
            "u": {"value": 1.66053906660e-27, "unit": "kg", "description": "Atomic mass unit"},
            
            # Universal constants
            "G": {"value": 6.67430e-11, "unit": "m³/kg⋅s²", "description": "Gravitational constant"},
            "k": {"value": 1.380649e-23, "unit": "J/K", "description": "Boltzmann constant"},
            "NA": {"value": 6.02214076e23, "unit": "1/mol", "description": "Avogadro constant"},
            "R": {"value": 8.314462618, "unit": "J/mol⋅K", "description": "Gas constant"},
            
            # Electromagnetic constants
            "eps0": {"value": 8.8541878128e-12, "unit": "F/m", "description": "Vacuum permittivity"},
            "mu0": {"value": 1.25663706212e-6, "unit": "H/m", "description": "Vacuum permeability"},
            "ke": {"value": 8.9875517923e9, "unit": "N⋅m²/C²", "description": "Coulomb constant"},
            
            # Other important constants
            "g": {"value": 9.80665, "unit": "m/s²", "description": "Standard gravity"},
            "atm": {"value": 101325, "unit": "Pa", "description": "Standard atmosphere"},
            "sigma": {"value": 5.670374419e-8, "unit": "W/m²⋅K⁴", "description": "Stefan-Boltzmann constant"},
            
            # Mathematical constants used in physics
            "pi": {"value": 3.141592653589793, "unit": "dimensionless", "description": "Pi"},
            "euler": {"value": 2.718281828459045, "unit": "dimensionless", "description": "Euler's number"}
        }
        
        # Common physics formulas
        self.formulas = {
            "kinetic_energy": {
                "formula": "KE = (1/2) * m * v²",
                "variables": {"m": "mass (kg)", "v": "velocity (m/s)"},
                "description": "Kinetic energy of an object"
            },
            "potential_energy": {
                "formula": "PE = m * g * h",
                "variables": {"m": "mass (kg)", "g": "gravity (m/s²)", "h": "height (m)"},
                "description": "Gravitational potential energy"
            },
            "force": {
                "formula": "F = m * a",
                "variables": {"m": "mass (kg)", "a": "acceleration (m/s²)"},
                "description": "Newton's second law"
            },
            "gravitational_force": {
                "formula": "F = G * m1 * m2 / r²",
                "variables": {"G": "gravitational constant", "m1": "mass 1 (kg)", "m2": "mass 2 (kg)", "r": "distance (m)"},
                "description": "Newton's law of universal gravitation"
            },
            "coulomb_law": {
                "formula": "F = k * q1 * q2 / r²",
                "variables": {"k": "Coulomb constant", "q1": "charge 1 (C)", "q2": "charge 2 (C)", "r": "distance (m)"},
                "description": "Coulomb's law for electrostatic force"
            },
            "ohms_law": {
                "formula": "V = I * R",
                "variables": {"V": "voltage (V)", "I": "current (A)", "R": "resistance (Ω)"},
                "description": "Ohm's law"
            },
            "wave_equation": {
                "formula": "v = f * λ",
                "variables": {"v": "wave speed (m/s)", "f": "frequency (Hz)", "λ": "wavelength (m)"},
                "description": "Wave equation"
            },
            "ideal_gas": {
                "formula": "PV = nRT",
                "variables": {"P": "pressure (Pa)", "V": "volume (m³)", "n": "moles", "R": "gas constant", "T": "temperature (K)"},
                "description": "Ideal gas law"
            }
        }
    
    async def execute(self, query: str, query_type: str = "constant") -> ToolResult:
        """
        Look up physics constants or formulas
        
        Args:
            query: Name/symbol of constant or formula to look up
            query_type: "constant", "formula", or "search"
            
        Returns:
            ToolResult with the requested information
        """
        try:
            query = query.lower().strip()
            
            if query_type == "constant":
                return await self._lookup_constant(query)
            elif query_type == "formula":
                return await self._lookup_formula(query)
            elif query_type == "search":
                return await self._search_all(query)
            else:
                return ToolResult(
                    success=False,
                    result=None,
                    error_message=f"Invalid query type: {query_type}. Use 'constant', 'formula', or 'search'"
                )
                
        except Exception as e:
            return ToolResult(
                success=False,
                result=None,
                error_message=f"Physics lookup error: {str(e)}"
            )
    
    async def _lookup_constant(self, symbol: str) -> ToolResult:
        """Look up a specific physics constant"""
        if symbol in self.constants:
            constant = self.constants[symbol]
            return ToolResult(
                success=True,
                result={
                    "symbol": symbol,
                    "value": constant["value"],
                    "unit": constant["unit"],
                    "description": constant["description"]
                },
                metadata={"type": "constant"}
            )
        else:
            # Try to find similar constants
            suggestions = [k for k in self.constants.keys() if symbol in k or k in symbol]
            return ToolResult(
                success=False,
                result=None,
                error_message=f"Constant '{symbol}' not found",
                metadata={"suggestions": suggestions[:5]}
            )
    
    async def _lookup_formula(self, name: str) -> ToolResult:
        """Look up a physics formula"""
        if name in self.formulas:
            formula_data = self.formulas[name]
            return ToolResult(
                success=True,
                result=formula_data,
                metadata={"type": "formula"}
            )
        else:
            # Try to find similar formulas
            suggestions = [k for k in self.formulas.keys() if name in k or k in name]
            return ToolResult(
                success=False,
                result=None,
                error_message=f"Formula '{name}' not found",
                metadata={"suggestions": suggestions[:5]}
            )
    
    async def _search_all(self, query: str) -> ToolResult:
        """Search through both constants and formulas"""
        results = {
            "constants": [],
            "formulas": []
        }
        
        # Search constants
        for symbol, data in self.constants.items():
            if (query in symbol.lower() or 
                query in data["description"].lower() or
                query in data["unit"].lower()):
                results["constants"].append({
                    "symbol": symbol,
                    "value": data["value"],
                    "unit": data["unit"],
                    "description": data["description"]
                })
        
        # Search formulas
        for name, data in self.formulas.items():
            if (query in name.lower() or 
                query in data["description"].lower() or
                query in data["formula"].lower()):
                results["formulas"].append({
                    "name": name,
                    **data
                })
        
        total_results = len(results["constants"]) + len(results["formulas"])
        
        if total_results > 0:
            return ToolResult(
                success=True,
                result=results,
                metadata={
                    "type": "search",
                    "total_results": total_results,
                    "query": query
                }
            )
        else:
            return ToolResult(
                success=False,
                result=None,
                error_message=f"No results found for '{query}'"
            )
    
    def list_all_constants(self) -> List[str]:
        """Get list of all available constants"""
        return list(self.constants.keys())
    
    def list_all_formulas(self) -> List[str]:
        """Get list of all available formulas"""
        return list(self.formulas.keys()) 