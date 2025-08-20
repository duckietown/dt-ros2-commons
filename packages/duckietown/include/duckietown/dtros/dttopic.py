"""Base utilities shared by DTROS publishers and subscribers."""

from __future__ import annotations

import time
from typing import Optional

from .constants import (
    TopicDirection,
    TopicType,
    MIN_TOPIC_FREQUENCY_SUPPORTED,
    MAX_TOPIC_FREQUENCY_SUPPORTED,
)
from .diagnostics import DTROSDiagnostics
from .singleton import get_instance


class DTTopic:
    """Common functionality for publishers and subscribers.

    The original ROS 1 implementation inherited from ``rospy.topics.Topic``.
    For ROS 2 this class simply keeps some bookkeeping information used for
    diagnostics and frequency estimation.
    """

    def __init__(self, name: str, **kwargs):
        self.resolved_name = name
        self._dt_healthy_freq = -1
        self._dt_topic_type = TopicType.GENERIC
        self._dt_is_ghost = False
        self._dt_help = None
        self._node = get_instance()
        if self._node is None:
            raise ValueError(
                "Cannot create an object of type DTTopic before a DTROS node is initialized."
            )
        self._parse_dt_args(kwargs)
        # topic statistics
        self._last_frequency_tick = -1.0
        self._frequency = 0.0

    def _parse_dt_args(self, kwargs):
        self._dt_healthy_freq = kwargs.get("dt_healthy_hz", -1)
        self._dt_topic_type = kwargs.get("dt_topic_type", TopicType.GENERIC)
        self._dt_is_ghost = kwargs.get("dt_ghost", False)
        self._dt_help = kwargs.get("dt_help", None)

    def _register_dt_topic(self, direction: TopicDirection):
        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().register_topic(
                self.resolved_name,
                self._dt_help,
                direction,
                self._dt_healthy_freq,
                self._dt_topic_type,
                self,
            )

    def set_healthy_freq(self, healthy_hz: int) -> None:
        self._dt_healthy_freq = healthy_hz
        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().update_topic(
                self.resolved_name, healthy_freq=self._dt_healthy_freq
            )

    def get_frequency(self) -> float:
        return self._frequency

    def get_bandwidth(self) -> float:
        if DTROSDiagnostics.enabled():
            return DTROSDiagnostics.getInstance().get_topic_bandwidth(self.resolved_name)
        return -1.0

    def _tick_frequency(self) -> None:
        if self._last_frequency_tick > 0:
            elapsed = time.time() - self._last_frequency_tick
            frequency = float(self._frequency * 0.3 + (1.0 / elapsed) * 0.7)
            if MIN_TOPIC_FREQUENCY_SUPPORTED <= frequency <= MAX_TOPIC_FREQUENCY_SUPPORTED:
                self._frequency = frequency
            else:
                self._frequency = 0.0
        self._last_frequency_tick = time.time()

    def shutdown(self) -> None:
        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().unregister_topic(self.resolved_name)

