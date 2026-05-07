#!/bin/bash

# Plant Disease Classification System - Quick Start Script for Linux/Mac

echo ""
echo "========================================"
echo "Plant Disease Classification System"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.13+ from https://www.python.org/"
    exit 1
fi

echo "Python found!"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "What would you like to do?"
echo ""
echo "1. Train the model (required on first run)"
echo "2. Run the Flask application"
echo "3. Exit"
echo ""

read -p "Enter your choice (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "Starting model training..."
        echo "This may take several hours on first run."
        echo ""
        python train_model.py
        if [ $? -ne 0 ]; then
            echo "ERROR: Model training failed"
            exit 1
        fi
        echo ""
        echo "Training complete!"
        ;;
    2)
        echo ""
        echo "Checking if model exists..."
        if [ ! -f "models/plant_disease_model.h5" ]; then
            echo "ERROR: Model not found!"
            echo "Please train the model first by running this script and selecting option 1."
            exit 1
        fi
        echo ""
        echo "Starting Flask application..."
        echo ""
        echo "Open your browser and go to: http://localhost:5000"
        echo ""
        echo "Press CTRL+C to stop the application."
        echo ""
        python app.py
        ;;
    3)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac
