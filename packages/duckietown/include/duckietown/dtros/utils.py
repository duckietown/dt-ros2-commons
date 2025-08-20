"""Helper utilities for ROS 2 based DTROS nodes.

The original ROS 1 implementation exposed a number of helpers to interact with
``rospy`` internals.  ROS 2 does not provide or require access to those
internals so the functionality is greatly simplified.  Only a small set of
utility helpers are kept for backwards compatibility.
"""

from __future__ import annotations

import os
from typing import Optional

from .singleton import get_instance


def get_ros_handler(*_, **__):  # pragma: no cover - kept for API compatibility
    """Return the underlying ROS handler.

    In ROS 1 this function returned the master handler used to subscribe to
    parameter updates.  With ROS 2 and ``rclpy`` this concept no longer exists,
    hence this function simply returns ``None``.  The signature is kept for
    backwards compatibility with code expecting it.
    """

    return None


def get_namespace(level: int) -> str:
    """Return the namespace up to a given depth.

    Parameters
    ----------
    level: int
        Number of namespace components to include starting from the root.
    """

    node = get_instance()
    if node is None:
        return "/"
    full_name = node.get_fully_qualified_name().lstrip("/")
    namespace_comps = full_name.split("/")
    if level > len(namespace_comps):
        level = len(namespace_comps)
    return "/%s" % "/".join(namespace_comps[:level])


def apply_namespace(name: str, ns_level: int) -> str:
    """Prepend the requested namespace to *name*.

    Parameters
    ----------
    name: str
        Resource name to qualify.
    ns_level: int
        Desired namespace depth.
    """

    return "%s/%s" % (get_namespace(ns_level).rstrip("/"), name.strip("/"))


def get_module_type() -> str:
    """Return the DT module type from the environment if available."""

    return os.environ.get("DT_MODULE_TYPE", "")


def get_module_instance() -> str:
    """Return the container identifier for the running module."""

    return os.environ.get("DT_MODULE_INSTANCE", "")

