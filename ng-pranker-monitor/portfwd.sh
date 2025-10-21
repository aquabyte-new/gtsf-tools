#!/usr/bin/env bash
set -euo pipefail

# SSH host
HOST=${1:-bergen}

echo "Forwarding ports to $HOST ..."

# Ports to forward
# Syntax: "local_addr:local_port:remote_addr:remote_port"
PORTS=(
  "localhost:8765:localhost:8765"
  "localhost:17171:localhost:17171"
  "localhost:17172:localhost:17172"
)

# Start each forward in the background
for p in "${PORTS[@]}"; do
  echo "Forwarding $p ..."
  ssh -N -L "$p" "$HOST" &
done

# Trap to clean up on exit
trap 'echo "Stopping all forwards..."; kill $(jobs -p)' SIGINT SIGTERM EXIT

# Wait for all background jobs
wait
