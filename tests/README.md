# Test Structure

This directory contains actual test files for the dt-ros2-commons project.

## Structure

- `test_ros/` - Unit and integration tests for ROS2 functionality
  - `test_communication.py` - Tests publisher/subscriber communication
  - `test_launch.py` - Tests launch file functionality

## Running Tests

### Unit Tests
```bash
cd /path/to/dt-ros2-commons
python -m pytest tests/
```

### Or with Python unittest
```bash
cd tests/test_ros
python -m unittest test_communication.py
python -m unittest test_launch.py
```

## Note

The actual ROS2 packages are located in `../packages/` directory, not here.
This `tests/` directory should only contain test files, not full ROS packages.
