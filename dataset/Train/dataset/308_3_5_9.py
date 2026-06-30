import os
from typing import NamedTuple



    pass


def should_skipped_by_specs(path):
    basename = os.path.basename(path)
    return (basename == ".") or (basename == "..")
