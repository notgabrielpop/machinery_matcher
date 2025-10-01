#!/bin/bash

# Machinery Matcher - Quick Installation Script
# For macOS and Linux

set -e

echo "=========================================="
echo "🎯 Machinery Matcher Installation"
echo "=========================================="
echo ""

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found!"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create config from example
if [ ! -f "config.py" ]; then
    echo ""
    echo "Creating config.py from template..."
    cp config.py.example config.py
    echo "✅ Created config.py"
    echo ""
    echo "⚠️  IMPORTANT: Edit config.py and add your Anthropic API key!"
    echo "   Get one from: https://console.anthropic.com"
else
    echo ""
    echo "ℹ️  config.py already exists, skipping..."
fi

# Create data directory
mkdir -p data
mkdir -p output

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit config.py and add your API key"
echo "2. Add your prospects.csv file"
echo "3. Run the dashboard:"
echo "   python3 machinery_dashboard.py"
echo "   Then open: http://localhost:5000"
echo ""
echo "Or run command line:"
echo "   python3 machinery_matcher.py"
echo ""
echo "=========================================="
