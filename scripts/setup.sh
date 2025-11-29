#!/bin/bash

# ============================================================================
# MCP Foundry ML Integration Setup Script
# ============================================================================
# This script automates the setup process for the MCP Foundry ML project.
# It checks prerequisites, installs dependencies, and configures the environment.
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ============================================================================
# Check Prerequisites
# ============================================================================

print_header "Checking Prerequisites"

# Check Python version
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.9+ required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

# Check Azure CLI
print_info "Checking Azure CLI..."
if command -v az &> /dev/null; then
    AZ_VERSION=$(az version --output tsv --query '"azure-cli"')
    print_success "Azure CLI found: $AZ_VERSION"
else
    print_warning "Azure CLI not found. Install from: https://aka.ms/install-azure-cli"
fi

# Check if virtual environment exists
print_info "Checking for virtual environment..."
if [ -d "venv" ]; then
    print_success "Virtual environment found"
else
    print_warning "No virtual environment found"
fi

# ============================================================================
# Create Virtual Environment
# ============================================================================

print_header "Setting Up Python Environment"

if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Using existing virtual environment"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "pip upgraded"

# ============================================================================
# Install Dependencies
# ============================================================================

print_header "Installing Dependencies"

print_info "Installing required packages..."
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    print_success "All dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# ============================================================================
# Configure Environment
# ============================================================================

print_header "Configuring Environment"

if [ ! -f ".env" ]; then
    print_info "Creating .env file from template..."
    cp .env.example .env
    print_success ".env file created"
    print_warning "Please edit .env file with your Azure credentials"
    print_info "Required variables:"
    echo "  - AZURE_SUBSCRIPTION_ID"
    echo "  - AZURE_RESOURCE_GROUP"
    echo "  - AZURE_ML_WORKSPACE"
    echo "  - PROJECT_ENDPOINT"
    echo "  - MODEL_DEPLOYMENT_NAME"
else
    print_info ".env file already exists"
fi

# ============================================================================
# Verify Azure Authentication
# ============================================================================

print_header "Verifying Azure Authentication"

if command -v az &> /dev/null; then
    print_info "Checking Azure authentication status..."
    
    if az account show &> /dev/null; then
        SUBSCRIPTION=$(az account show --query name -o tsv)
        print_success "Authenticated to Azure"
        print_info "Current subscription: $SUBSCRIPTION"
    else
        print_warning "Not authenticated to Azure"
        print_info "Run: az login"
    fi
else
    print_warning "Azure CLI not available - skipping authentication check"
fi

# ============================================================================
# Final Summary
# ============================================================================

print_header "Setup Complete!"

echo "Next steps:"
echo ""
echo "1. Configure your environment:"
echo "   ${GREEN}nano .env${NC}  # Edit with your Azure credentials"
echo ""
echo "2. Authenticate with Azure (if not already done):"
echo "   ${GREEN}az login${NC}"
echo "   ${GREEN}az account set --subscription <your-subscription-id>${NC}"
echo ""
echo "3. Ensure you have an Azure ML compute cluster named 'cpu-cluster'"
echo "   Or update aml/jobs/pipeline.yml with your cluster name"
echo ""
echo "4. Start the MCP server:"
echo "   ${GREEN}python server.py${NC}"
echo ""
echo "5. In another terminal, run the Foundry Agent demo:"
echo "   ${GREEN}python mcp_foundry_agent.py${NC}"
echo ""

print_success "Setup script completed successfully!"

# Deactivate virtual environment
deactivate 2>/dev/null || true
