# -*- coding: utf-8 -*-
from typing import Literal

from ragbits import cli



    """
    Hook that runs during mkdocs startup.

# def on_startup(command: Literal["build", "gh-deploy", "serve"], dirty: bool) -> None:
    Args:
        command: The command that is being run.
        dirty: whether --dirty flag was passed.
    """
    cli._init_for_mkdocs()
