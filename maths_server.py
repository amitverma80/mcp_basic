#!/usr/bin/env python3
"""
Sample MCP Calculator Server implementation in Python.

This module demonstrates how to create a simple MCP server with calculator tools
that can perform basic arithmetic operations (add, subtract, multiply, divide).
"""

from mcp.server.fastmcp import FastMCP


# Create a FastMCP server
mcp = FastMCP(name="MCP Maths Server",
              host="127.0.0.1",
              port=8000)

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add/Sum/+ two numbers together and return the result."""
    print("Adding", a, "and", b)
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract/- b from a and return the result."""
    print("Subtracting", b, "from", a)
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together and return the result."""
    print("Multiplying", a, "and", b)
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide a by b and return the result.
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    # Start the server with stdio transport
   mcp.run(transport="streamable-http", mount_path="/mcp")
