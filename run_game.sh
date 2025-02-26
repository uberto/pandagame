#!/bin/bash

# Script to run the Panda Escape Adventure game with a clean environment

echo "Starting Panda Escape Adventure game setup..."

# Unset Python environment variables that might cause conflicts
if [ -n "$PYTHONHOME" ]; then
    echo "Unsetting PYTHONHOME: $PYTHONHOME"
    unset PYTHONHOME
fi

if [ -n "$PYTHONPATH" ]; then
    echo "Unsetting PYTHONPATH: $PYTHONPATH"
    unset PYTHONPATH
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install it first:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Detected Python version: $PYTHON_VERSION"

# Try to use Python 3.13 specifically if available
if command -v python3.13 &> /dev/null; then
    echo "Python 3.13 found, using it explicitly..."
    poetry env use python3.13
    PYTHON_CMD="python3.13"
else
    echo "Python 3.13 not found in PATH, using default Python..."
    PYTHON_CMD="python3"
fi

# Create a virtual environment if it doesn't exist
if ! poetry env info &> /dev/null; then
    echo "Creating Poetry virtual environment..."
    poetry env use $PYTHON_CMD
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Run the game
echo "Starting the game..."
poetry run $PYTHON_CMD main.py

# Check exit status
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "Game exited with error code: $EXIT_CODE"
    echo "For troubleshooting, try setting DEBUG=True in the .env file"
    exit $EXIT_CODE
fi 