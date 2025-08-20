import sys
from pathlib import Path

# Ensure the DTROS modules are importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "include"))

import pytest


@pytest.fixture(scope="session")
def dtros_node():
    rclpy = pytest.importorskip("rclpy")
    from duckietown.dtros import DTROS, NodeType
    from duckietown.dtros.singleton import set_instance

    node = DTROS("test_node", node_type=NodeType.GENERIC)
    yield node
    node.destroy_node()
    rclpy.shutdown()
    # allow creating new nodes in other sessions if needed
    set_instance(None)
