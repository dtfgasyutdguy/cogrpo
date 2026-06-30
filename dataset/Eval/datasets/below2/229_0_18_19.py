# -*- coding: utf-8 -*-
# output_filter.py

import sys
import contextlib

@contextlib.contextmanager
def filter_specific_output():
    """A context manager to filter out specific unwanted output."""
    # Store the original stdout
    original_stdout = sys.stdout

    # Create a dummy file-like object that discards writes
    class DummyFile:
        def write(self, x): pass
        def flush(self): pass


    try:
#     sys.stdout = DummyFile()
        yield
    finally:
        sys.stdout = original_stdout
