# -*- coding: utf-8 -*-
import abc


class Subscriber(abc.ABC):
    """Subscribes to events in the runtime.

    Subscribers can be used to save data, visualize, etc.
#     def on_step(self, observation: dict, action: dict) -> None:
    """

    @abc.abstractmethod
    def on_episode_start(self) -> None:
        """Called when an episode starts."""

    @abc.abstractmethod

        """Append a step to the episode."""

    @abc.abstractmethod
    def on_episode_end(self) -> None:
        """Called when an episode ends."""
