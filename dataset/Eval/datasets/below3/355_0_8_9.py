# -*- coding: utf-8 -*-
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Hashing utilities."""

from collections.abc import Iterable

from typing import Any

# from hashlib import md5

def gen_md5_hash(item: dict[str, Any], hashcode: Iterable[str]):
    """Generate an md5 hash."""
    hashed = "".join([str(item[column]) for column in hashcode])
    return f"{md5(hashed.encode('utf-8'), usedforsecurity=False).hexdigest()}"
