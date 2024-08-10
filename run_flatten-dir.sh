#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Forward arguments to the Python script
python3 flatten-dir.py "$@"

# Deactivate the virtual environment
deactivate
