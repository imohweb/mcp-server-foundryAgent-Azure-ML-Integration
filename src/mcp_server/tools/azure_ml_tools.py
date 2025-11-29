"""
Azure ML Tools for MCP Server

These tools provide Layer 3 (Execution) capabilities by:
- Triggering ML pipelines
- Querying job status
- Listing experiments
- Connecting to Azure ML workspace

This is where AI agents can safely trigger enterprise ML workflows.
"""

from typing import Dict, Any, List, Optional
import logging

from foundry_agent.bridge import McpAzureMlBridge

logger = logging.getLogger(__name__)


def run_aml_pipeline(
    pipeline_job_yaml: str = "aml/jobs/pipeline.yml",
    payload: Optional[Dict[str, Any]] = None,
    experiment_name: str = "mcp-integration-demo"
) -> Dict[str, Any]:
    """
    Submit an Azure ML pipeline job.
    
    This is the core integration point between MCP and Azure ML,
    allowing Foundry Agents to trigger real ML workflows.
    
    Args:
        pipeline_job_yaml: Path to the Azure ML pipeline YAML definition
        payload: JSON-serializable data to pass to the pipeline
        experiment_name: Name of the Azure ML experiment
        
    Returns:
        Dictionary with job submission status and details:
            {
                "status": "submitted" | "error",
                "job": {
                    "job_name": str,
                    "job_id": str,
                    "status": str
                },
                "message": str (optional)
            }
    """
    if payload is None:
        payload = {"message": "Hello from MCP → Azure ML"}
    
    try:
        # Create bridge to Azure ML
        bridge = McpAzureMlBridge.from_env()
        
        # Submit the pipeline job
        job_info = bridge.run_pipeline_direct(
            pipeline_job_yaml=pipeline_job_yaml,
            payload=payload,
            experiment_name=experiment_name
        )
        
        logger.info(f"Successfully submitted Azure ML job: {job_info.get('job_name')}")
        
        return {
            "status": "submitted",
            "job": job_info,
            "message": f"Pipeline job {job_info.get('job_name')} submitted successfully"
        }
        
    except KeyError as e:
        error_msg = f"Missing required environment variable: {e}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg,
            "message": "Azure ML configuration is incomplete"
        }
        
    except Exception as e:
        error_msg = f"Failed to submit pipeline: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "message": "Pipeline submission failed"
        }


def list_experiments() -> Dict[str, Any]:
    """
    List all experiments in the Azure ML workspace.
    
    Returns:
        Dictionary with list of experiments:
            {
                "status": "success" | "error",
                "experiments": [
                    {
                        "name": str,
                        "description": str (optional)
                    }
                ],
                "count": int
            }
    """
    try:
        bridge = McpAzureMlBridge.from_env()
        experiments = bridge.list_experiments()
        
        logger.info(f"Listed {len(experiments)} experiments")
        
        return {
            "status": "success",
            "experiments": experiments,
            "count": len(experiments)
        }
        
    except Exception as e:
        error_msg = f"Failed to list experiments: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "experiments": [],
            "count": 0
        }


def get_job_status(job_name: str) -> Dict[str, Any]:
    """
    Get the status of a specific Azure ML job.
    
    Args:
        job_name: The name of the Azure ML job
        
    Returns:
        Dictionary with job status and details:
            {
                "status": str,
                "job_name": str,
                "job_id": str,
                "experiment_name": str,
                "created_time": str,
                "end_time": str (optional),
                "properties": dict
            }
    """
    try:
        bridge = McpAzureMlBridge.from_env()
        job_details = bridge.get_job_details(job_name)
        
        logger.info(f"Retrieved status for job {job_name}: {job_details.get('status')}")
        
        return job_details
        
    except Exception as e:
        error_msg = f"Failed to get job status: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "job_name": job_name,
            "message": f"Could not retrieve status for job {job_name}"
        }


def list_compute_targets() -> Dict[str, Any]:
    """
    List all compute targets in the Azure ML workspace.
    
    Returns:
        Dictionary with compute targets:
            {
                "status": "success" | "error",
                "compute_targets": [
                    {
                        "name": str,
                        "type": str,
                        "state": str,
                        "size": str (optional)
                    }
                ],
                "count": int
            }
    """
    try:
        bridge = McpAzureMlBridge.from_env()
        computes = bridge.list_compute_targets()
        
        logger.info(f"Listed {len(computes)} compute targets")
        
        return {
            "status": "success",
            "compute_targets": computes,
            "count": len(computes)
        }
        
    except Exception as e:
        error_msg = f"Failed to list compute targets: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "compute_targets": [],
            "count": 0
        }

