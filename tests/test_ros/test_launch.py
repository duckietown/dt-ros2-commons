#!/usr/bin/env python3

import unittest
import subprocess
import time
import os


class TestLaunchFiles(unittest.TestCase):
    def setUp(self):
        self.process = None

    def tearDown(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

    def test_simple_launch(self):
        """Test that the simple launch file starts without errors"""
        
        # Get the package path
        package_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'packages', 'test_ros'
        )
        
        # Start the launch file
        cmd = ['ros2', 'launch', 'test_ros', 'simple.launch.py']
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Let it run for a short time
            time.sleep(3)
            
            # Check if process is still running (good sign)
            self.assertIsNone(self.process.poll(), "Launch file terminated unexpectedly")
            
        except subprocess.CalledProcessError as e:
            self.fail(f"Launch file failed to start: {e}")


if __name__ == '__main__':
    unittest.main()
