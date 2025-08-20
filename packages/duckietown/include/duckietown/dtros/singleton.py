"""Singleton utilities for DTROS nodes.

This module keeps track of the single active :class:`duckietown.dtros.DTROS`
instance.  In ROS 1 this information used to be stored inside the ``rospy``
module directly.  ROS 2 does not expose such a handle so we simply keep a
global reference here.
"""

from __future__ import annotations

from typing import Optional


_instance: Optional[object] = None


def set_instance(node: object) -> None:
    """Register the currently running DTROS node.

    Parameters
    ----------
    node: object
        The instantiated :class:`duckietown.dtros.DTROS` object.
    """

    global _instance
    _instance = node


def get_instance() -> Optional[object]:
    """Return the active DTROS instance if any."""

    return _instance

