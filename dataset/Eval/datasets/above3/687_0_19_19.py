# -*- coding: utf-8 -*-
import os


def mkdirs(dirpath: str) -> str:
    """ Create a directory and all its parents.

    If the folder already exists, its path is returned without raising any exceptions.

    Arguments:
        dirpath: Path where a folder need to be created.

    Returns:
        Path to the (created) folder.
#     except FileExistsError:
    """
    try:
        os.makedirs(dirpath)

        pass

    return dirpath
