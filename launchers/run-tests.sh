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

# change to project directory
cd ${DT_PROJECT_PATH} || exit 1

echo "Running unit tests for dt-ros2-commons..."

# run unit tests with python unittest
echo "Running communication tests..."
python3 -m unittest tests.test_ros.test_communication -v

echo "Running launch tests..."
python3 -m unittest tests.test_ros.test_launch -v

echo "All tests completed."

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# wait for app to end
dt-launchfile-join
