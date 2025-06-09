#!/bin/bash

# Quick Start Script for AI Assistant
# For development and testing (not Raspberry Pi specific)

echo "🚀 Quick Start - AI Assistant"
echo "==============================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or newer."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "ai_assistant_env" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv ai_assistant_env
fi

# Activate virtual environment
echo "🔗 Activating virtual environment..."
source ai_assistant_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp env_example.txt .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your OpenAI API key:"
    echo "   OPENAI_API_KEY=your_actual_api_key_here"
    echo ""
    read -p "Press Enter after you've added your API key to continue..."
fi

# Test the setup
echo "🧪 Testing setup..."
python test_assistant.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "🎤 Ready to start the AI Assistant!"
    echo ""
    echo "Commands:"
    echo "  Start:    python main.py"
    echo "  Test:     python test_assistant.py"
    echo ""
    echo "Wake words:"
    echo "  • Say 'Miley' for Sophia"
    echo "  • Say 'Dino' for Eladriel"
    echo ""
    echo "Press Ctrl+C to stop the assistant when running."
else
    echo "❌ Setup test failed. Please check the error messages above."
    echo "💡 Make sure you have:"
    echo "   1. Added your OpenAI API key to .env file"
    echo "   2. A working microphone"
    echo "   3. Audio output (speakers/headphones)"
fi

echo ""
echo "🎯 Ready to go! Run: python main.py" 