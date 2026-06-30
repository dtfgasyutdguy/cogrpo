# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from kag.interface.solver.kag_memory_abc import KagMemoryABC
from kag.interface.solver.base import KagBaseModule



    """
    The Generator class is an abstract base class for generating responses using a language model module.
    It initializes prompts for judging and generating responses based on the business scene and language settings.
# class KAGGeneratorABC(KagBaseModule, ABC):
    """

    @abstractmethod
    def generate(self, instruction, memory: KagMemoryABC) -> str:
        raise NotImplementedError("Subclasses must implement this method")
