"""
MCP Server Main Implementation

This is the Layer 2 (Integration) component that:
- Exposes Python functions as MCP tools
- Routes calls from Foundry Agents to enterprise systems
- Enforces tool boundaries and validation
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import uvicorn

from .config import get_mcp_server_config
from .tools import utility_tools, azure_ml_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
config = get_mcp_server_config()
app = FastAPI(
    title=config.name,
    description="MCP Server for Foundry Agent Integration - Layer 2 (Integration)",
    version="1.0.0"
)


# ============================================================================
# Request/Response Models
# ============================================================================

class ToolRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]


class ToolResponse(BaseModel):
    status: str
    result: Any
    error: Optional[str] = None


# ============================================================================
# Layer 2: MCP Tool Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with server information"""
    return HTMLResponse(content=f"""
    <html>
        <head><title>{config.name}</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
            <h1>🤖 {config.name}</h1>
            <p>Layer 2 (Integration) - MCP Server for Microsoft Foundry Agents → Azure ML</p>
            
            <h2>Available Tools:</h2>
            <ul>
                <li><code>greet(name: str)</code> - Greet someone by name</li>
                <li><code>add_numbers(a: float, b: float)</code> - Add two numbers</li>
                <li><code>run_aml_pipeline(...)</code> - Trigger Azure ML pipeline</li>
                <li><code>list_aml_experiments()</code> - List experiments</li>
                <li><code>get_aml_job_status(job_name: str)</code> - Get job status</li>
            </ul>
            
            <h2>API Endpoints:</h2>
            <ul>
                <li><a href="/tools">/tools</a> - List all available tools</li>
                <li><a href="/docs">/docs</a> - Interactive API documentation</li>
                <li><code>POST /mcp/call</code> - Call a tool</li>
            </ul>
            
            <p><strong>Status:</strong> ✅ Server is running</p>
        </body>
    </html>
    """)


@app.get("/tools")
async def list_tools():
    """List all available MCP tools"""
    return {
        "tools": [
            {
                "name": "greet",
                "description": "Greet someone by name",
                "parameters": {"name": "string"}
            },
            {
                "name": "add_numbers",
                "description": "Add two numbers together",
                "parameters": {"a": "float", "b": "float"}
            },
            {
                "name": "run_aml_pipeline",
                "description": "Trigger an Azure ML pipeline job",
                "parameters": {
                    "pipeline_job_yaml": "string (optional)",
                    "payload": "dict (optional)",
                    "experiment_name": "string (optional)"
                }
            },
            {
                "name": "list_aml_experiments",
                "description": "List all experiments in Azure ML workspace",
                "parameters": {}
            },
            {
                "name": "get_aml_job_status",
                "description": "Get the status of an Azure ML job",
                "parameters": {"job_name": "string"}
            }
        ]
    }


@app.post("/mcp/call", response_model=ToolResponse)
async def call_tool(request: ToolRequest):
    """
    Call an MCP tool with parameters
    
    This is the main endpoint that Foundry Agents use to execute tools
    """
    tool_name = request.tool_name
    params = request.parameters
    
    logger.info(f"[MCP] Tool call: {tool_name} with params: {params}")
    
    try:
        # Route to the appropriate tool
        if tool_name == "greet":
            result = greet(**params)
        elif tool_name == "add_numbers":
            result = add_numbers(**params)
        elif tool_name == "run_aml_pipeline":
            result = run_aml_pipeline(**params)
        elif tool_name == "list_aml_experiments":
            result = list_aml_experiments()
        elif tool_name == "get_aml_job_status":
            result = get_aml_job_status(**params)
        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        return ToolResponse(status="success", result=result)
    
    except Exception as e:
        logger.error(f"[MCP] Error executing {tool_name}: {e}", exc_info=True)
        return ToolResponse(status="error", result=None, error=str(e))


# ============================================================================
# Tool Implementations
# ============================================================================

def greet(name: str) -> str:
    """
    Greet someone by name.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A greeting message
    """
    logger.info(f"[TOOL] greet called with name={name}")
    return utility_tools.greet(name)


def add_numbers(a: float, b: float) -> Dict[str, Any]:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Dictionary with the sum and inputs
    """
    logger.info(f"[TOOL] add_numbers called with a={a}, b={b}")
    return utility_tools.add_numbers(a, b)


def run_aml_pipeline(
    pipeline_job_yaml: str = "aml/jobs/pipeline.yml",
    payload: Dict[str, Any] = None,
    experiment_name: str = "mcp-integration-demo"
) -> Dict[str, Any]:
    """
    Trigger an Azure ML pipeline job.
    
    This is the core Layer 3 (Execution) integration that:
    - Loads a pipeline YAML definition
    - Injects agent data (payload)
    - Submits a job to Azure ML
    - Returns job details back to the agent
    
    Args:
        pipeline_job_yaml: Path to the Azure ML pipeline YAML file
        payload: Data to pass to the pipeline (JSON-serializable dict)
        experiment_name: Name of the Azure ML experiment
        
    Returns:
        Dictionary with job status and details
    """
    logger.info(
        f"[MCP TOOL] run_aml_pipeline called with "
        f"pipeline_job_yaml={pipeline_job_yaml}, "
        f"experiment_name={experiment_name}"
    )
    
    if payload is None:
        payload = {"message": "Hello from MCP → Azure ML"}
    
    try:
        result = azure_ml_tools.run_aml_pipeline(
            pipeline_job_yaml=pipeline_job_yaml,
            payload=payload,
            experiment_name=experiment_name
        )
        logger.info(f"[MCP TOOL] Azure ML job submitted: {result}")
        return result
    except Exception as e:
        logger.error(f"[MCP TOOL] Error running pipeline: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to submit Azure ML pipeline job"
        }


def list_aml_experiments() -> Dict[str, Any]:
    """
    List all experiments in the Azure ML workspace.
    
    Returns:
        Dictionary with list of experiments
    """
    logger.info("[TOOL] list_aml_experiments called")
    
    try:
        result = azure_ml_tools.list_experiments()
        logger.info(f"[TOOL] Found {len(result.get('experiments', []))} experiments")
        return result
    except Exception as e:
        logger.error(f"[TOOL] Error listing experiments: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "experiments": []
        }


def get_aml_job_status(job_name: str) -> Dict[str, Any]:
    """
    Get the status of an Azure ML job.
    
    Args:
        job_name: The name of the Azure ML job
        
    Returns:
        Dictionary with job status and details
    """
    logger.info(f"[TOOL] get_aml_job_status called with job_name={job_name}")
    
    try:
        result = azure_ml_tools.get_job_status(job_name)
        logger.info(f"[TOOL] Job {job_name} status: {result.get('status')}")
        return result
    except Exception as e:
        logger.error(f"[TOOL] Error getting job status: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to get status for job {job_name}"
        }


# ============================================================================
# Server Startup
# ============================================================================

def run_server():
    """
    Start the MCP server with HTTP transport.
    
    This creates HTTP endpoints that Foundry Agents and web browsers
    can access to call MCP tools.
    """
    logger.info(f"Starting {config.name}")
    logger.info(f"\nServer will be available at:")
    logger.info(f"  - http://localhost:{config.port}/")
    logger.info(f"  - http://0.0.0.0:{config.port}/")
    logger.info(f"\nKey Endpoints:")
    logger.info(f"  - GET  /           - Server info page")
    logger.info(f"  - GET  /tools      - List all tools")
    logger.info(f"  - POST /mcp/call   - Execute a tool")
    logger.info(f"  - GET  /docs       - API documentation")
    logger.info("\nRegistered tools:")
    logger.info("  - greet(name: str)")
    logger.info("  - add_numbers(a: float, b: float)")
    logger.info("  - run_aml_pipeline(pipeline_job_yaml, payload, experiment_name)")
    logger.info("  - list_aml_experiments()")
    logger.info("  - get_aml_job_status(job_name: str)")
    logger.info("\n" + "="*60)
    logger.info(f"Server starting on http://{config.host}:{config.port}")
    logger.info("="*60 + "\n")
    
    # Run the FastAPI server with uvicorn
    uvicorn.run(
        "mcp_server.main:app",  # Import string for reload support
        host=config.host,
        port=config.port,
        log_level="info",
        reload=True  # Enable auto-reload for development
    )


if __name__ == "__main__":
    run_server()
