"""
Utility Tools for MCP Server

These are simple demonstration tools that show basic MCP functionality.
They serve as examples of Layer 2 (Integration) tools.
"""

from typing import Dict, Any


def greet(name: str) -> str:
    """
    Generate a friendly greeting message.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A personalized greeting message
    """
    return f"Hello, {name}! Welcome to the MCP Foundry ML integration."


def add_numbers(a: float, b: float) -> Dict[str, Any]:
    """
    Add two numbers and return the result with metadata.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Dictionary containing:
            - sum: The sum of a and b
            - inputs: The original input values
            - operation: Description of the operation
    """
    result = a + b
    return {
        "sum": result,
        "inputs": {"a": a, "b": b},
        "operation": f"{a} + {b} = {result}"
    }


def multiply_numbers(a: float, b: float) -> Dict[str, Any]:
    """
    Multiply two numbers and return the result with metadata.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Dictionary containing the product and inputs
    """
    result = a * b
    return {
        "product": result,
        "inputs": {"a": a, "b": b},
        "operation": f"{a} × {b} = {result}"
    }
