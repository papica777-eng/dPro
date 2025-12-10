#!/bin/bash

# Simple run script for dPro QA Assistant

echo "=== dPro QA Assistant - Quick Start ==="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for serviceAccountKey.json
if [ ! -f "serviceAccountKey.json" ]; then
    echo ""
    echo "⚠️  WARNING: serviceAccountKey.json not found!"
    echo "   The application will run in DEMO mode without Firebase."
    echo "   To enable full functionality, add your Firebase service account key."
    echo ""
fi

# Run the application
echo ""
echo "Starting application..."
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
