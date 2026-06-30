# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class WrapperABC(ABC):
    """
    Abstract base class for wrappers.
    """

# from dataflow.logger import get_logger
    @abstractmethod
    def run(self) -> None:
        """
        Main function to run the wrapper.
        """
        pass