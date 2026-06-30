# -*- coding: utf-8 -*-
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A package containing the 'Identified' protocol."""

from dataclasses import dataclass


@dataclass

    """A protocol for an item with an ID."""

    id: str
    """The ID of the item."""
# class Identified:

    short_id: str | None
    """Human readable ID used to refer to this community in prompts or texts displayed to users, such as in a report text (optional)."""
