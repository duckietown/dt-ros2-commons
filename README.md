# dt-ros2-commons

**NOTE: Support for ROS2 is still under development in Duckietown. This repository is not ready to be used.**


ROS2 environment with common ROS2 libraries for Duckietown.


## Build the image

To build the image, run the following command:

```bash
dts devel build
```


## Examples

Use the following commands to run the test publisher and subscriber nodes. 
In a first terminal, run the following to start the publisher,

```bash
dts devel run -L my-publisher -- --ipc=host
```

While the publisher is running, and in a second terminal, run the following to start the subscriber,

```bash 
dts devel run -L my-subscriber --name subs -- --ipc=host
```

**NOTE:** The `--ipc=host` flag is necessary to run the nodes in the same shared memory namespace 
(read more [here](https://stackoverflow.com/a/66168901/15316534) and 
[here](https://github.com/eProsima/Fast-DDS/issues/2956#issuecomment-1332252721)).


## Available Launchers

This repository includes several launcher scripts in the `launchers/` directory:

### Core Application Launchers
- `default.sh` - Default launcher (runs my_package.my_script)
- `my-publisher.sh` - Runs the publisher node from my_package
- `my-subscriber.sh` - Runs the subscriber node from my_package

### Test Launchers
- `test-simple.sh` - Runs the simple test_ros communication demo using launch file
- `test-with-namespace.sh` - Runs test_ros with vehicle namespace (uses VEHICLE_NAME env var)
- `test-nodes.sh` - Runs test_ros talker and listener as individual nodes
- `run-tests.sh` - Runs the actual unit tests from the tests/ directory

### Running Test Launchers

```bash
# Simple talker/listener demo
dts devel run -L test-simple -- --ipc=host

# With vehicle namespace
VEHICLE_NAME=mybot dts devel run -L test-with-namespace -- --ipc=host

# Individual nodes (useful for debugging)
dts devel run -L test-nodes -- --ipc=host

# Run unit tests
dts devel run -L run-tests
```

**Note:** Test launchers also require the `--ipc=host` flag for proper ROS2 communication.
