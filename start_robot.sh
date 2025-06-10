#!/bin/bash
# AI Assistant Startup Script with Visual Feedback

# Source environment variables
source "$(dirname "$0")/robot_env.sh"

# Change to AI assistant directory
cd "$(dirname "$0")"

# Start the AI Assistant
echo "🤖 Starting AI Assistant with Visual Feedback..."
python3 main.py

# If that fails, try the integration example
if [ $? -ne 0 ]; then
    echo "⚠️  Main assistant failed, running integration example..."
    cd tests
    python3 integration_example.py
fi
