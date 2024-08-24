#!/bin/bash

# Deactivate the current virtual environment if it's active
deactivate 2>/dev/null

echo "deactivated"

# Remove the existing virtual environment directory
rm -rf venv/

echo "venv folder removed"

# Create a new virtual environment
python3 -m venv venv/


echo "new venv folder generated"

# Activate the new virtual environment
source venv/bin/activate

echo "activate new venv"

# Install the required packages
pip install -r requirements.txt

echo "requirements installed"

