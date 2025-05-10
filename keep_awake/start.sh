#!/bin/bash

# Script to start the matrix multiplication worker with proper logging

# Define log directory and file
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/output.log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Start the process with nohup, redirecting output to log file
echo "Starting matrix multiplication worker..."
echo "Logs will be written to $LOG_FILE"

# Start with unbuffered Python output (-u flag) to ensure real-time logging
nohup python -u keep_awake.py > "$LOG_FILE" 2>&1 &

# Store the PID in a variable
PID=$!

# Display info to the user
echo "Process started with PID: $PID"
echo "To view logs in real-time, run: tail -f $LOG_FILE"
echo "To terminate the process, run: ./termination.sh"