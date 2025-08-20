"""Duckietown aware wrapper around :mod:`rclpy` subscriptions."""

from __future__ import annotations

from typing import Any, Callable

from rclpy.subscription import Subscription

import humanfriendly

from .constants import TopicDirection
from .diagnostics import DTROSDiagnostics
from .dttopic import DTTopic
from .singleton import get_instance


class DTSubscriber(DTTopic):
    """A subscription that can be paused and resumed."""

    def __init__(
        self,
        name: str,
        data_class,
        callback: Callable[[Any], None],
        qos_profile: int = 10,
        **kwargs,
    ) -> None:
        super().__init__(name, **kwargs)
        node = get_instance()
        self._user_callback = callback
        self._subscription: Subscription = node.create_subscription(
            data_class, name, self._monitored_callback, qos_profile
        )
        self._active = True
        if not self._dt_is_ghost:
            self._register_dt_topic(TopicDirection.INBOUND)
        node._register_subscriber(self)  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, new_status: bool) -> None:
        self._active = new_status
        if DTROSDiagnostics.enabled():
            DTROSDiagnostics.getInstance().set_topic_switch(self.resolved_name, new_status)

    def switch_off(self) -> None:
        self.active = False

    def switch_on(self) -> None:
        self.active = True

    def anybody_publishing(self) -> bool:
        return self._subscription.get_publisher_count() > 0

    # ------------------------------------------------------------------
    def _monitored_callback(self, msg) -> None:
        if not self.active:
            return
        if self._user_callback:
            with get_instance().profiler(f"/auto/topic/callback{self.resolved_name}"):
                self._user_callback(msg)
        self._tick_frequency()

