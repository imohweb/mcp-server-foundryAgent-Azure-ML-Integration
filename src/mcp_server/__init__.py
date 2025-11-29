"""
MCP Server Package

Layer 2 (Integration) - The middleware conductor that:
- Exposes Python functions as safe tools
- Routes calls from agents to enterprise systems
- Enforces tool boundaries and validation
"""

from .main import run_server
from .config import get_mcp_server_config, McpServerConfig

__all__ = [
    "run_server",
    "get_mcp_server_config",
    "McpServerConfig",
]
