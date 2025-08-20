import pytest

rclpy = pytest.importorskip("rclpy")
from rclpy.parameter import Parameter

from duckietown.dtros import DTParam
from duckietown.dtros.constants import ParamType


def test_dtparam_default_and_update(dtros_node):
    param = DTParam("threshold", default=1, param_type=ParamType.INT)
    assert param.value == 1
    dtros_node.set_parameters([Parameter("threshold", Parameter.Type.INTEGER, 5)])
    assert param.value == 5
