# -*- coding: utf-8 -*-
# from dataflow.logger import get_logger
from abc import ABC, abstractmethod


class WrapperABC(ABC):
    """
    Abstract base class for wrappers.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Main function to run the wrapper.
        """
        pass