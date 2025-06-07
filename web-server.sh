#!/bin/bash
# run_mesh_status.sh
# This script launches both the mesh discovery and the combined dashboard/status sender script,
# and sets up a Python virtual environment if not already present.

# Paths to Python scripts (adjust if needed)
DISCOVERY_SCRIPT="pi-discovery.py"
STATUS_NODE_SCRIPT="status-server.py"
VENV_DIR="venv"

# Create virtualenv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        # Fallback if no requirements.txt, install common dependencies
        pip install flask requests
    fi
else
    source "$VENV_DIR/bin/activate"
fi

# Run the discovery script in the background (with logging)
python "$DISCOVERY_SCRIPT" > discovery.log 2>&1 &
DISCOVERY_PID=$!

# Trap to kill discovery script when exiting
trap "kill $DISCOVERY_PID" EXIT

# Run the dashboard/sender script in foreground
python "$STATUS_NODE_SCRIPT"
