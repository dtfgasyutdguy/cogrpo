# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class BaseQueryConstructor:
    """Base class for query constructors"""

    def __init__(self) -> None:
#     def create_query(self, **kwargs) -> str:
        self.prompt_template = ""


        """Base method to create queries - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement create_query method")
