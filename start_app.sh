#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate virtual environment
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "Activating virtual environment..."
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Virtual environment 'venv' not found. Please run setup first."
    exit 1
fi

# Start Flask app in the background
echo "Starting Flask web server (for adding ingredients)..."
python "$SCRIPT_DIR/app.py" &
FLASK_PID=$!
echo "Flask app running with PID $FLASK_PID. Access it at http://127.0.0.1:5000/"

# Function to clean up background process on exit
cleanup() {
    echo "Stopping Flask web server (PID $FLASK_PID)..."
    kill $FLASK_PID
    # Deactivate virtual environment if it was activated by this script
    if type deactivate > /dev/null 2>&1; then
        echo "Deactivating virtual environment..."
        deactivate
    fi
    echo "Exiting."
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM to run cleanup
trap cleanup SIGINT SIGTERM

# Start CLI app in the foreground
echo "Starting CLI application..."
python "$SCRIPT_DIR/main_cli.py"

# Cleanup after CLI finishes (if not interrupted by Ctrl+C)
cleanup
