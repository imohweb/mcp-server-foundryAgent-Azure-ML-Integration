"""
Bridge between MCP and Azure Machine Learning.

This module focuses on Azure ML only (no MCP client inside) so that
MCP tools (e.g. run_aml_pipeline) can call into it to submit pipeline jobs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict

from azure.ai.ml import MLClient, load_job
from azure.identity import DefaultAzureCredential


@dataclass
class AzureMlConfig:
    """Configuration for connecting to an Azure ML workspace."""
    subscription_id: str
    resource_group: str
    workspace_name: str


class McpAzureMlBridge:
    """
    Helper class for submitting pipeline jobs to Azure ML.

    Typical usage from an MCP tool:
        bridge = McpAzureMlBridge.from_env()
        result = bridge.run_pipeline_direct("aml/jobs/pipeline.yml", payload)
    """

    def __init__(self, ml_client: MLClient):
        self.ml_client = ml_client

    # ---------------------------------------------------------------------
    # Factory method to build the bridge from environment variables
    # ---------------------------------------------------------------------
    @classmethod
    def from_env(cls) -> "McpAzureMlBridge":
        """
        Create a McpAzureMlBridge using configuration from environment variables.

        Required environment variables:
            AZURE_SUBSCRIPTION_ID
            AZURE_RESOURCE_GROUP
            AZURE_ML_WORKSPACE
        """
        cfg = AzureMlConfig(
            subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
            resource_group=os.environ["AZURE_RESOURCE_GROUP"],
            workspace_name=os.environ["AZURE_ML_WORKSPACE"],
        )

        credential = DefaultAzureCredential()
        ml_client = MLClient(
            credential=credential,
            subscription_id=cfg.subscription_id,
            resource_group_name=cfg.resource_group,
            workspace_name=cfg.workspace_name,
        )
        return cls(ml_client)

    # ---------------------------------------------------------------------
    # Direct pipeline execution helper
    # ---------------------------------------------------------------------
    def run_pipeline_direct(
        self,
        pipeline_job_yaml: str,
        payload: Dict[str, Any],
        experiment_name: str = "mcp-integration-demo",
    ) -> Dict[str, Any]:
        """
        Submit a pipeline job to Azure ML with 'payload' passed as an input parameter.

        Assumptions:
            - The pipeline defined in `pipeline_job_yaml` has an input named 'input_data'.
            - `payload` is JSON-serializable (e.g., dict, list, basic types).

        Args:
            pipeline_job_yaml: Path to the Azure ML pipeline job YAML file.
            payload: Data to be passed into the pipeline as the 'input_data' input.
            experiment_name: Name of the Azure ML experiment to associate with the job.

        Returns:
            A dictionary with basic job metadata:
                {
                    "job_name":  <job name>,
                    "job_id":    <job ARM ID>,
                    "status":    <job status>,
                }
        """
        # Load the pipeline job definition from YAML
        job = load_job(pipeline_job_yaml)

        # Note: Pipeline no longer accepts inputs - payload is ignored
        # The pipeline is designed to run as a simple demo without dynamic inputs
        
        # Set experiment name if not already specified in the YAML
        if getattr(job, "experiment_name", None) is None:
            job.experiment_name = experiment_name

        # Submit the job to Azure ML
        submitted = self.ml_client.jobs.create_or_update(job)

        # Return a simplified view of the job details (sanitized - no subscription ID)
        return {
            "job_name": submitted.name,
            "status": submitted.status,
            "experiment_name": getattr(submitted, "experiment_name", None),
        }

    # ---------------------------------------------------------------------
    # Additional Azure ML operations for MCP tools
    # ---------------------------------------------------------------------

    def list_experiments(self) -> list[Dict[str, Any]]:
        """
        List all experiments in the workspace.

        Returns:
            List of dictionaries with experiment details
        """
        experiments = []
        try:
            # In newer Azure ML SDK, experiments are accessed through jobs
            # Get unique experiment names from jobs
            jobs = self.ml_client.jobs.list()
            experiment_names = set()
            
            for job in jobs:
                if hasattr(job, 'experiment_name') and job.experiment_name:
                    experiment_names.add(job.experiment_name)
            
            for exp_name in sorted(experiment_names):
                experiments.append({
                    "name": exp_name,
                    "description": None,
                })
        except Exception as e:
            # If there are no jobs yet, return empty list
            pass
            
        return experiments

    def get_job_details(self, job_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific job.

        Args:
            job_name: The name of the job to retrieve

        Returns:
            Dictionary with comprehensive job details
        """
        job = self.ml_client.jobs.get(job_name)
        
        # Return sanitized job details (no subscription ID or full ARM paths)
        return {
            "job_name": job.name,
            "status": job.status,
            "experiment_name": getattr(job, "experiment_name", None),
            "created_time": str(job.creation_context.created_at) if hasattr(job, "creation_context") else None,
            "display_name": getattr(job, "display_name", None),
            "duration": str(getattr(job, "duration", "N/A")),
        }

    def list_compute_targets(self) -> list[Dict[str, Any]]:
        """
        List all compute targets in the workspace.

        Returns:
            List of dictionaries with compute target details
        """
        computes = []
        for compute in self.ml_client.compute.list():
            computes.append({
                "name": compute.name,
                "type": compute.type,
                "state": getattr(compute, "provisioning_state", "unknown"),
                "size": getattr(compute, "size", None),
            })
        return computes
