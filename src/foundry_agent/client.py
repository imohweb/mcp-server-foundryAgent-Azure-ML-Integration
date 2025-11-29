"""
Client script to demonstrate Microsoft Foundry Agents calling MCP tools.

This uses:
- AIProjectClient (azure-ai-projects)
- MCP integration for tool calling via HTTP requests

Note: This implementation uses direct HTTP calls to the MCP server
to demonstrate the agent <-> MCP <-> Azure ML workflow.
"""

import os
import time
import logging
import json
import requests

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _call_mcp_tool(tool_name: str, parameters: dict) -> dict:
    """
    Call an MCP tool via HTTP request.
    
    Args:
        tool_name: Name of the tool to call
        parameters: Parameters for the tool
        
    Returns:
        Tool execution result
    """
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp/call")
    
    try:
        response = requests.post(
            mcp_server_url,
            json={
                "tool_name": tool_name,
                "parameters": parameters
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to call MCP tool {tool_name}: {e}")
        return {"status": "error", "error": str(e)}


def _build_mcp_tool():
    """
    Configure MCP tool connection for the Foundry Agent.
    
    Returns configuration for connecting to the MCP server.
    """
    server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp/call")
    server_label = os.getenv("MCP_SERVER_LABEL", "local-mcp-server")

    logger.info(f"MCP Server URL: {server_url}")
    logger.info(f"MCP Server Label: {server_label}")

    # Return configuration dict
    return {
        "server_url": server_url,
        "server_label": server_label,
        "allowed_tools": ["greet", "add_numbers", "run_aml_pipeline", "list_aml_experiments", "get_aml_job_status"]
    }


def run_foundry_agent_demo() -> None:
    """
    End-to-end demo:
    - Connect to Microsoft Foundry Project
    - Create a thread and send a message
    - Simulate agent calling MCP tools to run ML pipeline
    
    This demonstrates the full workflow:
    User -> Foundry Agent -> MCP Server -> Azure ML
    """
    logger.info("Starting Foundry Agent Demo")
    logger.info("=" * 80)
    
    # Check for required environment variables
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_deployment_name = os.environ.get("MODEL_DEPLOYMENT_NAME")
    agent_id = os.environ.get("AGENT_ID")
    agent_name = os.environ.get("AGENT_NAME", "mcp-foundry-agent")
    api_key = os.environ.get("AZURE_AI_PROJECT_API_KEY")
    
    if not project_endpoint:
        logger.error("Missing required environment variable: PROJECT_ENDPOINT")
        logger.error("Please configure your .env file with the Foundry project endpoint.")
        return

    try:
        # Initialize credentials
        if api_key:
            credential = AzureKeyCredential(api_key)
            logger.info("Using API Key authentication")
        else:
            credential = DefaultAzureCredential()
            logger.info("Using DefaultAzureCredential authentication")
        
        mcp_config = _build_mcp_tool()
        
        logger.info("\n" + "=" * 80)
        logger.info("🚀 FOUNDRY AGENT + MCP SERVER + AZURE ML DEMO")
        logger.info("=" * 80)
        logger.info(f"Project Endpoint: {project_endpoint}")
        logger.info(f"Model Deployment: {model_deployment_name or 'Not specified'}")
        logger.info(f"Agent ID: {agent_id or 'Not configured'}")
        logger.info(f"Agent Name: {agent_name}")
        logger.info(f"MCP Server: {mcp_config['server_url']}")
        logger.info(f"Available Tools: {', '.join(mcp_config['allowed_tools'])}")
        logger.info("=" * 80)
        
        # Initialize AI Project Client
        logger.info("\n[1/5] Connecting to Azure AI Foundry...")
        try:
            client = AIProjectClient(
                credential=credential,
                endpoint=project_endpoint
            )
            logger.info("✓ Connected to Azure AI Foundry project")
        except Exception as init_error:
            logger.error(f"❌ Failed to connect: {init_error}")
            logger.info("\n💡 Falling back to direct MCP tool demonstration...")
            _demonstrate_mcp_tools_directly()
            return
        
        # Get user input
        logger.info("\n[2/5] User sends message to Foundry Agent...")
        print("\n" + "=" * 80)
        print("💬 Enter your message for the agent (or press Enter for default):")
        print("   Default: 'Hi, use the MCP server to run my ML pipeline'")
        print("=" * 80)
        user_input = input("Your message: ").strip()
        user_message = user_input if user_input else "Hi, use the MCP server to run my ML pipeline"
        logger.info(f"📝 User Message: \"{user_message}\"")
        
        logger.info("\n[3/5] Agent processes request and identifies required tools...")
        
        # Simple keyword-based tool selection (simulating agent intelligence)
        tool_name = None
        tool_params = {}
        
        if "pipeline" in user_message.lower() or "run" in user_message.lower():
            tool_name = "run_aml_pipeline"
            tool_params = {
                "pipeline_job_yaml": "aml/jobs/pipeline.yml",
                "payload": {"message": user_message},
                "experiment_name": "mcp-foundry-demo"
            }
            logger.info("🤖 Agent: \"I need to call the run_aml_pipeline tool via MCP server\"")
        elif "experiment" in user_message.lower() or "list" in user_message.lower():
            tool_name = "list_aml_experiments"
            tool_params = {}
            logger.info("🤖 Agent: \"I need to call the list_aml_experiments tool via MCP server\"")
        elif "status" in user_message.lower() or "job" in user_message.lower():
            logger.info("🤖 Agent: \"I need to call the get_aml_job_status tool via MCP server\"")
            job_name = input("\nEnter job name: ").strip()
            tool_name = "get_aml_job_status"
            tool_params = {"job_name": job_name}
        elif "greet" in user_message.lower() or "hello" in user_message.lower():
            tool_name = "greet"
            tool_params = {"name": "Azure Community"}
            logger.info("🤖 Agent: \"I need to call the greet tool via MCP server\"")
        else:
            tool_name = "run_aml_pipeline"
            tool_params = {
                "pipeline_job_yaml": "aml/jobs/pipeline.yml",
                "payload": {"message": user_message},
                "experiment_name": "mcp-foundry-demo"
            }
            logger.info("🤖 Agent: \"Defaulting to run_aml_pipeline tool via MCP server\"")
        
        logger.info(f"\n[4/5] Agent calls MCP Server -> {tool_name}...")
        result = _call_mcp_tool(tool_name, tool_params)
        
        logger.info("\n[5/5] MCP Server Response:")
        logger.info("=" * 80)
        logger.info(json.dumps(result, indent=2))
        logger.info("=" * 80)
        
        if result.get("status") == "success" and result.get("result", {}).get("status") == "submitted":
            job_info = result["result"]["job"]
            logger.info("\n✅ SUCCESS! ML Pipeline submitted to Azure ML")
            logger.info(f"Job Name: {job_info.get('job_name')}")
            logger.info(f"Status: {job_info.get('status')}")
            logger.info(f"Experiment: {job_info.get('experiment_name')}")
            
            logger.info("\n🎯 Complete workflow executed:")
            logger.info("   1. User -> Foundry Agent: Message sent")
            logger.info("   2. Foundry Agent -> MCP Server: Tool call")
            logger.info("   3. MCP Server -> Azure ML: Pipeline submitted")
            logger.info("   4. Azure ML: Job running on compute cluster")
        else:
            logger.warning("\n⚠️  Pipeline submission encountered an issue")
            logger.warning("Check the response above for details")
        
        logger.info("\n" + "=" * 80)
        logger.info("Demo completed! Check Azure ML portal for job status.")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"\n❌ Error running demo: {e}", exc_info=True)
        logger.error("\nTroubleshooting:")
        logger.error("1. Verify your Azure credentials: az login")
        logger.error("2. Check PROJECT_ENDPOINT format in .env")
        logger.error("3. Ensure MCP server is running: python server.py")
        logger.error("4. Ensure you have access to the Foundry project")


def _demonstrate_mcp_tools_directly():
    """
    Fallback demo that directly calls MCP tools without Foundry Agent.
    """
    logger.info("\n" + "=" * 80)
    logger.info("🔧 DIRECT MCP TOOLS DEMONSTRATION")
    logger.info("=" * 80)
    
    # Test 1: Greet
    logger.info("\n[Test 1] Calling greet tool...")
    result1 = _call_mcp_tool("greet", {"name": "Azure Community"})
    logger.info(f"Result: {json.dumps(result1, indent=2)}")
    
    # Test 2: Add numbers
    logger.info("\n[Test 2] Calling add_numbers tool...")
    result2 = _call_mcp_tool("add_numbers", {"a": 10, "b": 5})
    logger.info(f"Result: {json.dumps(result2, indent=2)}")
    
    # Test 3: Run pipeline
    logger.info("\n[Test 3] Calling run_aml_pipeline tool...")
    result3 = _call_mcp_tool("run_aml_pipeline", {
        "pipeline_job_yaml": "aml/jobs/pipeline.yml",
        "payload": {"message": "Direct MCP test"},
        "experiment_name": "mcp-direct-demo"
    })
    logger.info(f"Result: {json.dumps(result3, indent=2)}")
    
    logger.info("\n" + "=" * 80)
    logger.info("Direct MCP demonstration completed!")
    logger.info("=" * 80)
