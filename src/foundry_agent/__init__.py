"""
Foundry Agent Package

Layer 1 (Intelligence) - Contains:
- Client code for Microsoft Foundry Agents
- Bridge to Azure ML
- Agent configuration and orchestration
"""

from .client import run_foundry_agent_demo
from .bridge import McpAzureMlBridge, AzureMlConfig

__all__ = [
    "run_foundry_agent_demo",
    "McpAzureMlBridge",
    "AzureMlConfig",
]
