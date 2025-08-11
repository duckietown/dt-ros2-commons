#!/bin/bash

source /environment.sh

# initialize launch file
dt-launchfile-init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------

# NOTE: Use the variable DT_PROJECT_PATH to know the absolute path to your code
# NOTE: Use `dt-exec COMMAND` to run the main process (blocking process)

# set module's health
dt-set-module-healthy

# launching individual test nodes
echo "Launching test_ros individual nodes..."

# launch talker in background
ros2 run test_ros talker.py &
TALKER_PID=$!

# launch listener in background  
ros2 run test_ros listener.py &
LISTENER_PID=$!

# function to cleanup on exit
cleanup() {
    echo "Cleaning up test nodes..."
    kill $TALKER_PID $LISTENER_PID 2>/dev/null
    wait $TALKER_PID $LISTENER_PID 2>/dev/null
}

# trap cleanup on exit
trap cleanup EXIT

# wait for processes
wait $TALKER_PID $LISTENER_PID

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# wait for app to end
dt-launchfile-join
