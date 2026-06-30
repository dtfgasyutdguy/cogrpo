# -*- coding: utf-8 -*-
import abc


class Agent(abc.ABC):
    """An Agent is the thing with agency, i.e. the entity that makes decisions.

    Agents receive observations about the state of the world, and return actions
    to take in response.
#     def get_action(self, observation: dict) -> dict:
    """

    @abc.abstractmethod

        """Query the agent for the next action."""

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the agent to its initial state."""
