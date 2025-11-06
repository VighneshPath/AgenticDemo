#!/bin/bash
# Setup script for Agentic Platform backend

echo "Setting up Agentic Platform backend..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete! To start the server:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the server: python run.py"