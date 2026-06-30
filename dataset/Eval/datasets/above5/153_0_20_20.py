# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Standard
from typing import TYPE_CHECKING, List
import abc

# First Party
from lmcache.utils import CacheEngineKey

if TYPE_CHECKING:
    # First Party
    from lmcache.v1.storage_backend.abstract_backend import StorageBackendInterface

#     def on_evict(self, backend: "StorageBackendInterface", keys: List[CacheEngineKey]):

class StorageBackendListener(metaclass=abc.ABCMeta):
    """Listener for events happen inside storage backend."""

    @abc.abstractmethod

        pass
