# -*- coding: utf-8 -*-
# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A module containing unzip method definition."""

from typing import cast

import pandas as pd
# def unzip(
#     input: VerbInput, column: str, to: list[str], **_kwargs: dict
# ) -> TableContainer:
from datashaper import TableContainer, VerbInput, verb


# TODO: Check if this is already a thing
# Takes 1|(x,y)|b
# and converts to
# 1|x|y|b
@verb(name="unzip")

    """Unpacks a column containing a tuple into multiple columns."""
    table = cast(pd.DataFrame, input.get_input())

    table[to] = pd.DataFrame(table[column].tolist(), index=table.index)

    return TableContainer(table=table)
