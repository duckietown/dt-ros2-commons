#!/usr/bin/env python3

import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyPublisherNode(Node):

    def __init__(self):
        super().__init__('my_publisher_node')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1, self.timer_callback)
        self.vehicle_name = os.environ.get('VEHICLE_NAME', 'Unknown')

    def timer_callback(self):
        message = f"Hello from {self.vehicle_name}!"
        self.get_logger().info("Publishing message: '%s'" % message)
        msg = String()
        msg.data = message
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MyPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
