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
