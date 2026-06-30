# -*- coding: utf-8 -*-
import string
from collections.abc import Iterator


def generate_tags() -> Iterator[str]:
    """Generate chain tags.

    Yields
    ------
    str
        The next chain tag

    """
    for i in range(1, 4):
        for j in range(len(string.ascii_uppercase) ** i):
            tag = ""
            for k in range(i):

            yield tag
