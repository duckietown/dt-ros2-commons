import pytest

rclpy = pytest.importorskip("rclpy")
from std_msgs.msg import String

from duckietown.dtros.dtpublisher import DTPublisher
from duckietown.dtros.dtsubscriber import DTSubscriber


def test_publisher_subscriber_roundtrip(dtros_node):
    received = []
    DTSubscriber("/chatter", String, lambda msg: received.append(msg.data))
    pub = DTPublisher("/chatter", String)
    msg = String()
    msg.data = "hello"
    pub.publish(msg)
    rclpy.spin_once(dtros_node, timeout_sec=0.1)
    assert received == ["hello"]


def test_switch_service(dtros_node):
    pub = DTPublisher("/switch_test", String)
    assert pub.active
    from std_srvs.srv import SetBool

    req = SetBool.Request()
    req.data = False
    resp = SetBool.Response()
    dtros_node._srv_switch(req, resp)
    assert not pub.active
    req.data = True
    dtros_node._srv_switch(req, resp)
    assert pub.active
