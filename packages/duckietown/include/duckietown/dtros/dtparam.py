"""Parameter helper class for ROS 2."""

from __future__ import annotations

import json
from typing import Callable, List, Optional

from rclpy.parameter import Parameter

from . import get_instance
from .constants import ParamType
from .diagnostics import DTROSDiagnostics

MIN_MAX_SUPPORTED_TYPES = [ParamType.INT, ParamType.FLOAT]


class DTParam:
    def __init__(
        self,
        name: str,
        default=None,
        help: Optional[str] = None,
        param_type: ParamType = ParamType.UNKNOWN,
        min_value=None,
        max_value=None,
        __editable__: bool = True,
    ) -> None:
        self._name = name
        self._help = help
        self._editable = __editable__
        if not isinstance(param_type, ParamType):
            raise ValueError(
                "Parameter 'param_type' must be an instance of duckietown.ParamType. "
                f"Got {str(type(param_type))} instead."
            )
        self._type = param_type
        self._update_listeners: List[Callable[[], None]] = []

        # parse optional args
        if min_value is not None and param_type not in MIN_MAX_SUPPORTED_TYPES:
            raise ValueError(
                "Parameter 'min_value' not supported for parameter of type '%s'." % param_type.name
            )
        self._min_value = ParamType.parse(param_type, min_value)
        if max_value is not None and param_type not in MIN_MAX_SUPPORTED_TYPES:
            raise ValueError(
                "Parameter 'max_value' not supported for parameter of type '%s'." % param_type.name
            )
        self._max_value = ParamType.parse(param_type, max_value)
        self._default_value = ParamType.parse(param_type, default)
        if self._default_value is not None:
            if self._min_value is not None and self._default_value < self._min_value:
                raise ValueError(
                    "Given default value %s is below the min_value %s for parameter '%s'"
                    % (str(self._default_value), str(self._min_value), name)
                )
            if self._max_value is not None and self._default_value > self._max_value:
                raise ValueError(
                    "Given default value %s is above the max_value %s for parameter '%s'"
                    % (str(self._default_value), str(self._max_value), name)
                )
        if help is not None and not isinstance(help, str):
            raise ValueError(
                "Parameter 'help' in DTParam expects a value of type 'str', got '%s' instead."
                % (str(type(help)))
            )

        node = get_instance()
        if node is None:
            raise ValueError("You cannot create a DTParam object before initializing a DTROS object")

        if node.has_parameter(self._name):
            self._value = node.get_parameter(self._name).value
        else:
            if default is None:
                raise KeyError(f"Parameter `{self._name}` not found.")
            self._value = self._default_value
            node.declare_parameter(self._name, self._default_value)
        node._add_param(self)  # type: ignore[attr-defined]

        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().register_param(
                self._name,
                self._help,
                self._type,
                self._min_value,
                self._max_value,
                self._editable,
            )

    # ------------------------------------------------------------------
    def set_value(self, value):
        # update internal value
        self._value = value
        for cb in self._update_listeners:
            try:
                cb()
            except Exception as e:  # pragma: no cover - best effort
                get_instance().get_logger().error(  # type: ignore[attr-defined]
                    f"Parameter update callback {cb.__name__} resulted in error: {str(e)}"
                )

    def force_update(self):
        node = get_instance()
        if node is not None and node.has_parameter(self._name):
            self._value = node.get_parameter(self._name).value

    def options(self):
        options = {}
        if self.min_value is not None:
            options["min_value"] = self.min_value
        if self.max_value is not None:
            options["max_value"] = self.max_value
        return options

    def register_update_callback(self, cb):
        if cb is not None and callable(cb):
            self._update_listeners.append(cb)
        else:
            get_instance().get_logger().error(  # type: ignore[attr-defined]
                f"Callback for parameter {self._name} not registered because it is None or not callable!"
            )

    def unregister_update_callback(self, cb):
        if cb in self._update_listeners:
            self._update_listeners.remove(cb)

    # ------------------------------------------------------------------
    @property
    def name(self):
        return self._name

    @property
    def help(self):
        return self._help

    @property
    def value(self):
        return self._value

    @property
    def default(self):
        return self._default_value

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    @property
    def type(self):
        return self._type

    def __str__(self):
        return json.dumps(
            {
                "name": self.name,
                "help": self.help,
                "value": self.value,
                "default": self.default,
                "min_value": self.min_value,
                "max_value": self.max_value,
                "type": self.type.name,
                "_editable": self._editable,
            },
            sort_keys=True,
            indent=4,
        )

