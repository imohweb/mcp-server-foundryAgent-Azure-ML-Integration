#!/bin/bash

# Azure ML Compute Cluster Setup Script
# This script creates a compute cluster for running ML pipelines

set -e

echo "=========================================="
echo "Azure ML Compute Cluster Setup"
echo "=========================================="
echo ""

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo "📋 Configuration:"
echo "  Subscription: $AZURE_SUBSCRIPTION_ID"
echo "  Resource Group: $AZURE_RESOURCE_GROUP"
echo "  Workspace: $AZURE_ML_WORKSPACE"
echo "  Compute Name: mcp-compute"
echo ""

# Check if Azure CLI ML extension is installed
echo "🔍 Checking Azure CLI ML extension..."
if ! az extension list --query "[?name=='ml'].name" -o tsv | grep -q "ml"; then
    echo "Installing Azure ML extension..."
    az extension add --name ml --yes
else
    echo "✓ Azure ML extension already installed"
fi

echo ""
echo "🖥️  Creating compute cluster 'mcp-compute'..."
echo ""

# Create compute cluster
az ml compute create \
  --name mcp-compute \
  --type amlcompute \
  --size Standard_DS3_v2 \
  --min-instances 0 \
  --max-instances 2 \
  --idle-time-before-scale-down 120 \
  --resource-group $AZURE_RESOURCE_GROUP \
  --workspace-name $AZURE_ML_WORKSPACE

echo ""
echo "✅ Compute cluster 'mcp-compute' created successfully!"
echo ""
echo "📊 Cluster Details:"
echo "  - Name: mcp-compute"
echo "  - VM Size: Standard_DS3_v2 (4 cores, 14GB RAM)"
echo "  - Min Instances: 0 (auto-scales down when idle)"
echo "  - Max Instances: 2"
echo "  - Idle timeout: 120 seconds"
echo ""
echo "🎉 Your Azure ML workspace is now ready for pipeline execution!"
