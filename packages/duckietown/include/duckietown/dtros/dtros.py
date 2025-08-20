"""Main DTROS node class for ROS 2."""

from __future__ import annotations

from typing import Optional

import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from std_srvs.srv import SetBool
from ament_index_python.packages import (
    get_package_share_directory,
    PackageNotFoundError,
)

from duckietown_msgs.srv import (
    NodeGetParamsList,
    NodeRequestParamsUpdate,
)
from duckietown_msgs.msg import NodeParameter

from .dtparam import DTParam
from .constants import (
    NodeHealth,
    NodeType,
    NODE_SWITCH_SERVICE_NAME,
    NODE_GET_PARAM_SERVICE_NAME,
    NODE_REQUEST_PARAM_UPDATE_SERVICE_NAME,
)
from .diagnostics import DTROSDiagnostics
from .profiler import CodeProfiler
from .utils import get_ros_handler
from .singleton import set_instance, get_instance


class DTROS(Node):
    """Parent class for all Duckietown ROS 2 nodes."""

    def __init__(
        self,
        node_name: str,
        node_type: NodeType,
        pkg_name: Optional[str] = None,
        help: Optional[str] = None,
        dt_ghost: bool = False,
    ) -> None:
        if get_instance() is not None:
            raise RuntimeError("You cannot instantiate two objects of type DTROS")
        rclpy.init(args=None)  # no-op if already initialised
        super().__init__(node_name)
        set_instance(self)
        if not isinstance(node_type, NodeType):
            raise ValueError(
                "DTROS 'node_type' parameter must be of type 'duckietown.NodeType', "
                f"got {str(type(node_type))} instead."
            )
        self.node_name = self.get_fully_qualified_name()
        self.node_help = help
        self.node_type = node_type
        self.is_shutdown = False
        self._is_ghost = dt_ghost
        self._health = NodeHealth.STARTING
        self._health_reason: Optional[str] = None
        self._ros_handler = get_ros_handler()
        self._package_name = pkg_name

        # parameters
        self._parameters = dict()
        self.add_on_set_parameters_callback(self._param_update)

        # publishers/subscribers tracking
        self._switch = True
        self._subscribers = []
        self._publishers = []

        # create switch service and parameter services
        self.srv_switch = self.create_service(SetBool, NODE_SWITCH_SERVICE_NAME, self._srv_switch)
        self._srv_get_params = self.create_service(
            NodeGetParamsList, NODE_GET_PARAM_SERVICE_NAME, self._srv_get_params_list
        )
        self._srv_request_params_update = self.create_service(
            NodeRequestParamsUpdate, NODE_REQUEST_PARAM_UPDATE_SERVICE_NAME, self._srv_request_param_update
        )

        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().register_node(
                self.node_name, self.node_help, self.node_type, health=self._health
            )

        self.profiler = CodeProfiler()

        self.set_health(NodeHealth.STARTED)

    # ------------------------------------------------------------------
    @property
    def is_ghost(self) -> bool:
        return self._is_ghost

    @property
    def switch(self) -> bool:
        return self._switch

    @property
    def parameters(self):
        return list(self._parameters.values())

    @property
    def subscribers(self):
        return self._subscribers

    @property
    def publishers(self):
        return self._publishers

    @property
    def package_name(self) -> Optional[str]:
        return self._package_name

    @property
    def package_path(self) -> Optional[str]:
        if not self.package_name:
            return None
        try:
            return get_package_share_directory(self.package_name)
        except PackageNotFoundError:
            self.get_logger().warning(
                f"Could not determine the package path for {self.package_name}"
            )
            return None

    # ------------------------------------------------------------------
    def set_health(self, health: NodeHealth, reason: Optional[str] = None) -> None:
        if not isinstance(health, NodeHealth):
            raise ValueError(
                "Argument 'health' must be of type duckietown.NodeHealth. "
                f"Got {str(type(health))} instead"
            )
        self.log(f"Health status changed [{self._health.name}] -> [{health.name}]")
        self._health = health
        self._health_reason = None if reason is None else str(reason)
        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().update_node(
                health=self._health, health_reason=self._health_reason
            )

    # ------------------------------------------------------------------
    def log(self, msg: str, type: str = "info") -> None:
        full_msg = f"[{self.node_name}] {msg}"
        logger = self.get_logger()
        if type == "debug":
            logger.debug(full_msg)
        elif type == "info":
            logger.info(full_msg)
        elif type in ["warn", "warning"]:
            self.set_health(NodeHealth.WARNING, full_msg)
            logger.warning(full_msg)
        elif type in ["err", "error"]:
            self.set_health(NodeHealth.ERROR, full_msg)
            logger.error(full_msg)
        elif type == "fatal":
            self.set_health(NodeHealth.FATAL, full_msg)
            logger.fatal(full_msg)
        else:
            raise ValueError(f"Type argument value {type} is not supported!")

    def loginfo(self, msg):
        self.log(msg, type="info")

    def logerr(self, msg):
        self.log(msg, type="err")

    def logfatal(self, msg):
        self.log(msg, type="fatal")

    def logwarn(self, msg):
        self.log(msg, type="warn")

    def logdebug(self, msg):
        self.log(msg, type="debug")

    # ------------------------------------------------------------------
    def on_switch_on(self):
        pass

    def on_switch_off(self):
        pass

    def _srv_switch(self, request: SetBool.Request, response: SetBool.Response) -> SetBool.Response:
        old_state = self._switch
        self._switch = new_state = request.data
        for pub in self.publishers:
            pub.active = self._switch
        for sub in self.subscribers:
            sub.active = self._switch
        {False: self.on_switch_off, True: self.on_switch_on}[self._switch]()
        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().update_node(enabled=self._switch)
        msg = f"Node switched from [{'on' if old_state else 'off'}] to [{'on' if new_state else 'off'}]"
        self.log(msg)
        response.success = True
        response.message = msg
        return response

    # ------------------------------------------------------------------
    def _srv_get_params_list(self, request, response: NodeGetParamsList.Response):
        response.parameters = [
            NodeParameter(
                node=self.get_fully_qualified_name(),
                name=p.name,
                help=p.help,
                type=p.type.value,
                **p.options(),
            )
            for p in self.parameters
        ]
        return response

    def _srv_request_param_update(self, request, response: NodeRequestParamsUpdate.Response):
        try:
            self._parameters[request.parameter].force_update()
            response.success = True
        except KeyError:
            response.success = False
        return response

    # ------------------------------------------------------------------
    def _param_update(self, params):
        for param in params:
            name, value = param.name, param.value
            if name in self._parameters:
                self._parameters[name].set_value(value)
                self.loginfo(f'Parameter "{name}" has now the value [{self._parameters[name].value}]')
        return SetParametersResult(successful=True)

    # ------------------------------------------------------------------
    def _add_param(self, param: DTParam) -> None:
        if not isinstance(param, DTParam):
            raise ValueError(
                "Expected type duckietown.DTParam, got %s instead" % str(type(param))
            )
        self._parameters[param.name] = param

    def _has_param(self, param: str) -> bool:
        return param in self._parameters

    def _register_publisher(self, publisher) -> None:
        self._publishers.append(publisher)

    def _register_subscriber(self, subscriber) -> None:
        self._subscribers.append(subscriber)

    # ------------------------------------------------------------------
    def destroy_node(self) -> bool:
        result = super().destroy_node()
        self._on_shutdown()
        return result

    def _on_shutdown(self) -> None:
        self.log("Received shutdown request.")
        self.is_shutdown = True
        self.on_shutdown()

    def on_shutdown(self) -> None:  # pragma: no cover - user override
        pass

