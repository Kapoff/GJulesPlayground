#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
URL="http://127.0.0.1:5000/"

# Activate virtual environment
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "Activating virtual environment..."
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Virtual environment 'venv' not found. Please run setup first."
    exit 1
fi

echo "Starting Flask web server..."
# Run Flask app in the foreground. The script will wait here until Flask exits.
python "$SCRIPT_DIR/app.py" &
FLASK_PID=$!

# Give the server a moment to start before trying to open the browser
sleep 2

echo "Attempting to open web browser to $URL..."
# Try to open the URL in the default browser (cross-platform)
if command -v xdg-open > /dev/null; then
    xdg-open "$URL"
elif command -v gnome-open > /dev/null; then
    gnome-open "$URL"
elif command -v open > /dev/null; then # macOS
    open "$URL"
else
    echo "Could not detect a command to open the browser automatically."
    echo "Please open your web browser and navigate to $URL"
fi

echo "Flask app expected to be running with PID $FLASK_PID. Access it at $URL"
echo "Use the 'Shutdown Server' button in the web UI to stop the server and this script."

# Wait for the Flask process to exit
wait $FLASK_PID

# Deactivate virtual environment if it was activated by this script
if type deactivate > /dev/null 2>&1; then
    echo "Flask server has shut down."
    echo "Deactivating virtual environment..."
    deactivate
fi

echo "Exiting."
exit 0
