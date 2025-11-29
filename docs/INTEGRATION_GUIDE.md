# **MCP Server → Foundry AI Agent → Azure ML Pipeline Integration**

## **Complete Integration Flow Explanation** 🚀

---

## **Step 1: User Talks to Agent** 💬
```
User: "Run my ML pipeline"
```
The **Foundry Agent** (powered by GPT-4) understands natural language and decides which tool to call.

**Code Location:** `src/foundry_agent/client.py`

---

## **Step 2: Agent Calls MCP Server** 🔧
```python
# Agent sends HTTP request to MCP Server
POST http://localhost:8000/mcp/call
{
  "tool_name": "run_aml_pipeline",
  "parameters": {
    "pipeline_job_yaml": "aml/jobs/pipeline.yml",
    "experiment_name": "demo"
  }
}
```
The **MCP Server** acts as a secure gateway, exposing only safe, validated tools.

**Code Location:** `src/mcp_server/main.py` and `src/mcp_server/tools/azure_ml_tools.py`

---

## **Step 3: MCP Server Triggers Azure ML** ⚙️
```python
# src/foundry_agent/bridge.py
def run_pipeline_direct(pipeline_job_yaml, payload, experiment_name):
    # Load pipeline definition
    job = load_job(pipeline_job_yaml)
    
    # Submit to Azure ML
    submitted = ml_client.jobs.create_or_update(job)
    
    # Return job details
    return {
        "job_name": submitted.name,
        "status": submitted.status
    }
```
Azure ML executes the pipeline on the **compute cluster** (mcp-compute).

---

## **The Complete Flow in 10 Seconds**
```
User Message → Foundry Agent (understands intent)
              ↓
          MCP Server (validates & routes)
              ↓
          Azure ML (executes pipeline)
              ↓
          Response back to User
```

---

## **Why This Matters** 🎯

| Without MCP | With MCP |
|-------------|----------|
| ❌ Agent directly accesses Azure | ✅ Controlled through secure gateway |
| ❌ Hard to validate inputs | ✅ Validation built into tools |
| ❌ Difficult to audit | ✅ Every call logged and traceable |
| ❌ Security risks | ✅ Principle of least privilege |

**Key Point:** MCP is the "security guard" between AI and your enterprise systems! 🛡️

---

# **pipeline.yml Explanation** 📋

## **What It Does**
This YAML file defines a **simple demo pipeline** that Azure ML will execute on your compute cluster.

---

## **The Code**
```yaml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
description: Simple MCP → Azure ML pipeline demo

display_name: mcp_foundry_demo_pipeline
experiment_name: mcp-foundry-demo

jobs:
  process_data:
    type: command
    command: >-
      echo "MCP Foundry ML Pipeline Started" &&
      echo "Processing data from MCP Server" &&
      python -c "import json, sys; print('Pipeline Status: Success'); print('Executed via MCP Foundry Bridge'); sys.exit(0)"
    environment:
      image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest
    compute: azureml:mcp-compute
```

---

## **Breaking It Down**

| Section | What It Means |
|---------|---------------|
| **type: pipeline** | This is an Azure ML pipeline job |
| **display_name** | Name shown in Azure ML Studio |
| **experiment_name** | Groups related runs together |
| **jobs.process_data** | A single job in the pipeline |
| **type: command** | Runs shell commands |
| **command** | The actual work - prints messages and runs Python |
| **environment.image** | Docker container to use (Ubuntu 20.04 with Python) |
| **compute** | Run on `mcp-compute` cluster |

---

## **What Happens When It Runs** 🚀

1. Azure ML pulls the Docker image
2. Spins up a container on `mcp-compute` cluster
3. Executes the commands:
   - Prints "MCP Foundry ML Pipeline Started"
   - Prints "Processing data from MCP Server"
   - Runs Python code that prints success message
4. Job completes in ~3 minutes
5. Returns status to MCP Server → Agent → User

---

## **Why It's Simple** 💡
- **No inputs**: Removed complex parameter passing for demo clarity
- **No outputs**: Just prints messages to show execution
- **Quick execution**: ~3 minutes, perfect for live demos
- **Proof of concept**: Shows the integration works end-to-end

**In production**, you'd replace the `echo` commands with real ML code (training, data processing, etc.).
