"""
Configuration helpers for the MCP server.
"""

import os
from dataclasses import dataclass


@dataclass
class McpServerConfig:
    name: str = "MCP Foundry Bridge Server"
    host: str = "0.0.0.0"
    port: int = 8000
    path: str = "/mcp"


def get_mcp_server_config() -> McpServerConfig:
    return McpServerConfig(
        name=os.getenv("MCP_SERVER_NAME", "MCP Foundry Bridge Server"),
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8000")),
        path=os.getenv("MCP_SERVER_PATH", "/mcp"),
    )
