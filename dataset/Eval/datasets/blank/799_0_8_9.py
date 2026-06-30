# -*- coding: utf-8 -*-
import abc
from typing import Dict


class BasePolicy(abc.ABC):
    @abc.abstractmethod

        """Infer actions from observations."""

    def reset(self) -> None:
        """Reset the policy to its initial state."""
        pass
