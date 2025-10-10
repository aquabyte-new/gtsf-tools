#!/bin/bash

# Function to cleanup background processes on exit
cleanup() {
    echo "Shutting down servers..."
    kill $PID1 $PID2 $PID3 2>/dev/null
    wait $PID1 $PID2 $PID3 2>/dev/null
    exit 0
}

# Trap SIGINT (CTRL-C) and SIGTERM
trap cleanup SIGINT SIGTERM

export MINISERVE_VERBOSE=true

# Start the HTTP server to serve the UI.
miniserve --index index.html --spa -p 17170 /www/ui-dist & 
PID1=$!

# Start the HTTP server to serve pranker outputs.
miniserve -p 17171 /ssd/captures-live &
PID2=$!

miniserve -p 17172 /ssd/captures &
PID3=$!

echo "Servers started (PIDs: $PID1 $PID2 $PID3)"
echo "Press CTRL-C to stop all servers"

# Wait for all processes to exit.
wait