import re
import math
import operator
from typing import Union
from .base_tool import BaseTool, ToolResult

class CalculatorTool(BaseTool):
   #Calculator tool
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Performs safe mathematical calculations including basic arithmetic, trigonometry, and common math functions"
        )
        
        # Safe operations mapping
        self.safe_operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '^': operator.pow,
            'pow': pow,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'abs': abs,
            'ceil': math.ceil,
            'floor': math.floor,
            'round': round,
            'pi': math.pi,
            'e': math.e
        }
    
    async def execute(self, expression: str) -> ToolResult:
        """
        Safely evaluate a mathematical expression
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            ToolResult with calculation result
        """
        try:
            # Clean and validate the expression
            cleaned_expr = self._clean_expression(expression)
            
            if not self._is_safe_expression(cleaned_expr):
                return ToolResult(
                    success=False,
                    result=None,
                    error_message="Expression contains unsafe operations"
                )
            
            # Evaluate the expression
            result = self._safe_eval(cleaned_expr)
            
            return ToolResult(
                success=True,
                result=result,
                metadata={
                    "original_expression": expression,
                    "cleaned_expression": cleaned_expr,
                    "result_type": type(result).__name__
                }
            )
            
        except ZeroDivisionError:
            return ToolResult(
                success=False,
                result=None,
                error_message="Division by zero"
            )
        except ValueError as e:
            return ToolResult(
                success=False,
                result=None,
                error_message=f"Invalid mathematical operation: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                result=None,
                error_message=f"Calculation error: {str(e)}"
            )
    
    def _clean_expression(self, expression: str) -> str:
        """Clean and normalize the mathematical expression"""
        # Remove whitespace
        cleaned = re.sub(r'\s+', '', expression)
        
        # Replace common math notation
        cleaned = cleaned.replace('^', '**')  # Power notation
        cleaned = cleaned.replace('×', '*')   # Multiplication symbol
        cleaned = cleaned.replace('÷', '/')   # Division symbol
        
        return cleaned
    
    def _is_safe_expression(self, expression: str) -> bool:
        """Check if expression contains only safe operations"""
        # Allow only numbers, operators, parentheses, and safe function names
        safe_pattern = r'^[0-9+\-*/().\s^a-z_]*$'
        if not re.match(safe_pattern, expression, re.IGNORECASE):
            return False
        
        # Check for dangerous keywords
        dangerous_keywords = ['import', 'exec', 'eval', '__', 'open', 'file']
        for keyword in dangerous_keywords:
            if keyword in expression.lower():
                return False
        
        return True
    
    def _safe_eval(self, expression: str) -> Union[int, float]:
        """Safely evaluate mathematical expression using eval with restricted globals"""
        # Create safe namespace with only math functions
        safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "pow": pow,
            "max": max,
            "min": min,
        }
        
        # Add math functions
        for name in ['sin', 'cos', 'tan', 'sqrt', 'log', 'log10', 'ceil', 'floor', 'pi', 'e']:
            if hasattr(math, name):
                safe_dict[name] = getattr(math, name)
        
        # Evaluate with restricted namespace
        result = eval(expression, safe_dict, {})
        
        # Ensure result is a number
        if not isinstance(result, (int, float)):
            raise ValueError("Result is not a number")
        
        return result 