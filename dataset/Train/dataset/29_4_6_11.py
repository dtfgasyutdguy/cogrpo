import pytest

from sqlparse import utils



def test_remove_quotes(value, expected):
    assert utils.remove_quotes(value) == expected
