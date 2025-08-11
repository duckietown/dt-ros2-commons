#!/usr/bin/env python3

import unittest
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import threading


class TestTalkerListener(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = Node('test_node')
        self.received_messages = []

    def tearDown(self):
        self.node.destroy_node()

    def message_callback(self, msg):
        self.received_messages.append(msg.data)

    def test_publisher_subscriber_communication(self):
        """Test that publisher and subscriber can communicate"""
        
        # Create publisher
        publisher = self.node.create_publisher(String, 'test_chatter', 10)
        
        # Create subscriber
        subscription = self.node.create_subscription(
            String,
            'test_chatter',
            self.message_callback,
            10
        )

        # Spin in background
        executor = rclpy.executors.SingleThreadedExecutor()
        executor.add_node(self.node)
        
        def spin_thread():
            executor.spin()
        
        thread = threading.Thread(target=spin_thread, daemon=True)
        thread.start()

        # Publish a test message
        test_message = String()
        test_message.data = "Hello ROS2 Test!"
        
        # Give some time for subscription to be established
        time.sleep(0.5)
        
        publisher.publish(test_message)
        
        # Wait for message to be received
        time.sleep(0.5)
        
        # Check that message was received
        self.assertEqual(len(self.received_messages), 1)
        self.assertEqual(self.received_messages[0], "Hello ROS2 Test!")
        
        executor.shutdown()


if __name__ == '__main__':
    unittest.main()
