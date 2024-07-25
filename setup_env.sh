#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages..."
./venv/bin/pip install -r requirements.txt

echo "Environment setup complete. Virtual environment is activated."