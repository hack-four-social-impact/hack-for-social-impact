#!/bin/bash
# Quick Setup Script for Backend
# Run this from the main project directory: ./backend/quick-setup.sh

set -e  # Exit on any error

echo "🚀 PDF Backend Quick Setup"
echo "=========================="

# Check if we're in the right directory
if [[ ! -f "main.py" ]]; then
    echo "❌ Please run this script from the backend directory"
    echo "   cd main/backend && ./quick-setup.sh"
    exit 1
fi

echo "📍 Current directory: $(pwd)"

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.13"

if [[ $(echo "$python_version >= $required_version" | bc -l) -eq 0 ]]; then
    echo "⚠️  Warning: Python $required_version+ recommended, found $python_version"
else
    echo "✅ Python $python_version detected"
fi

# Create virtual environment
if [[ ! -d ".venv" ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn[standard] google-generativeai PyPDF2 python-multipart python-dotenv requests

# Create .env file if it doesn't exist
if [[ ! -f ".env" ]]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
EOF
    echo "✅ .env file created"
    echo "⚠️  IMPORTANT: Edit .env and add your real Gemini API key!"
else
    echo "✅ .env file already exists"
fi

# Test installation
echo "🧪 Testing installation..."
if python -c "import fastapi, uvicorn; print('✅ Core modules imported successfully')" 2>/dev/null; then
    echo "✅ Installation successful!"
else
    echo "❌ Installation test failed"
    exit 1
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your Gemini API key:"
echo "   GEMINI_API_KEY=your_actual_api_key_here"
echo ""
echo "2. Get your API key at: https://aistudio.google.com/"
echo ""
echo "3. Start the server:"
echo "   source .venv/bin/activate"
echo "   uvicorn main:app --reload"
echo ""
echo "4. Test at: http://localhost:8000/docs"
echo ""
echo "🔑 Don't forget to add your Gemini API key to the .env file!"