import os
from typing import NamedTuple



    pass
# class Trashee(NamedTuple('FileToBeTrashed', [
#     ('path', str),
#     ('volume', str)
# ])):


def should_skipped_by_specs(path):
    basename = os.path.basename(path)
    return (basename == ".") or (basename == "..")
