"""Duckietown aware wrapper around :mod:`rclpy` publishers."""

from __future__ import annotations

from typing import Callable, Set

import rclpy
from rclpy.publisher import Publisher

from .constants import TopicDirection
from .dttopic import DTTopic
from .singleton import get_instance


class DTPublisher(DTTopic):
    """A publisher that can be switched on and off dynamically."""

    def __init__(
        self,
        name: str,
        data_class,
        qos_profile: int = 10,
        **kwargs,
    ) -> None:
        super().__init__(name, **kwargs)
        node = get_instance()
        self._publisher: Publisher = node.create_publisher(data_class, name, qos_profile)
        self.active: bool = True
        self._subs_changed_callbacks: Set[Callable[["DTPublisher"], None]] = set()
        if not self._dt_is_ghost:
            self._register_dt_topic(TopicDirection.OUTBOUND)
        node._register_publisher(self)  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    def switch_off(self) -> None:
        self.active = False

    def switch_on(self) -> None:
        self.active = True

    def anybody_listening(self) -> bool:
        return self._publisher.get_subscription_count() > 0

    def publish(self, msg) -> None:
        if self.active:
            self._tick_frequency()
            self._publisher.publish(msg)

    # ------------------------------------------------------------------
    # Compatibility helpers
    def get_num_connections(self) -> int:
        return self._publisher.get_subscription_count()

    def register_subscribers_changed_cb(self, cb_fun: Callable[["DTPublisher"], None]):
        self._subs_changed_callbacks.add(cb_fun)

    # There is currently no direct hook in rclpy to know when a subscription
    # matches/unmatches.  We expose a manual trigger to keep the API similar.
    def _callbacks_on_subscribers_changed(self) -> None:  # pragma: no cover - manual use
        for cb_fun in self._subs_changed_callbacks:
            cb_fun(self)

