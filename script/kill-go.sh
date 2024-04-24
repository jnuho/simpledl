#!/bin/bash

# Replace 'app_name' with the name of your process
keyword="Go"

# Find the process ID (PID)
pid=$(ps -ef | grep $keyword | grep -v grep | awk '{print $2}')
appname=$(ps -ef | grep $keyword | grep -v grep | awk '{$1=$2=$3=$4=$5=""; print $0}')

# Check if the process is running
if [ -z "$pid" ]; then
    echo "Process $appname is not running."
else
    # Kill the process
    kill $pid
    echo "Process $appname (PID: $pid) has been terminated."
fi
