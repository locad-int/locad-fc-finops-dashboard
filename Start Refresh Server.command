#!/bin/bash
# Double-click this file in Finder to start the LOCAD Dashboard Refresh Server.
# Keep the Terminal window open while you want the Refresh button to work.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Starting LOCAD Dashboard Refresh Server..."
echo "Script dir: $SCRIPT_DIR"
echo ""
python3 "$SCRIPT_DIR/refresh_server.py"
echo ""
echo "Server stopped. Press any key to close."
read -n 1
