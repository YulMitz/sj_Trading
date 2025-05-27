#!/bin/bash

# Script to terminate all matrix multiplication worker processes

# Check if PID file exists
PID_FILE="matmul_worker.pid"
if [ ! -f "$PID_FILE" ]; then
    echo "PID file not found. No running process or it was started without PID tracking."
    echo "Attempting to find processes manually..."
    
    # Try to find processes by searching for python with our script name
    PIDS=$(ps -ef | grep "python" | grep -v grep | awk '{print $2}')
    if [ -z "$PIDS" ]; then
        echo "No matching processes found."
        exit 1
    fi
else
    # Read the main process PID
    MAIN_PID=$(cat "$PID_FILE")
    echo "Found main process with PID: $MAIN_PID"
    
    # Find all child processes
    PIDS=$(pstree -p $MAIN_PID | grep -o '([0-9]\+)' | grep -o '[0-9]\+')
    
    # Add the main PID to the list
    PIDS="$MAIN_PID $PIDS"

    # Add the main PID to the list
    PIDS="$MAIN_PID $PIDS"

    PID_PREFIX=${MAIN_PID:0:3}
    echo "Searching for all processes with PID starting with $PID_PREFIX..."

    # List all PIDs, filter those starting with PID_PREFIX, exclude already found PIDs
    EXTRA_PIDS=$(ps -e -o pid= | awk -v pre="$PID_PREFIX" '{if($1 ~ "^"pre) print $1}' | grep -v -w -e "$MAIN_PID" $(echo $PIDS | sed 's/ / -e /g'))

    if [ ! -z "$EXTRA_PIDS" ]; then
        echo "Also found these processes by PID prefix: $EXTRA_PIDS"
        PIDS="$PIDS $EXTRA_PIDS"
    fi
fi

# Count processes to terminate
COUNT=$(echo $PIDS | wc -w)
echo "Found $COUNT process(es) to terminate"

# Send SIGTERM to all processes
for PID in $PIDS; do
    echo "Terminating process $PID..."
    kill -15 $PID 2>/dev/null
done

# Wait a moment
echo "Waiting for processes to exit gracefully..."
sleep 5

# Check if processes are still running and force kill if necessary
for PID in $PIDS; do
    if kill -0 $PID 2>/dev/null; then
        echo "Process $PID did not terminate gracefully, force killing..."
        kill -9 $PID 2>/dev/null
    fi
done

# Clean up PID file
if [ -f "$PID_FILE" ]; then
    rm "$PID_FILE"
    echo "PID file removed."
fi

echo "Termination complete."