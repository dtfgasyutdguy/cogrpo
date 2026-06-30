import pytest

from sqlparse import utils



def test_remove_quotes(value, expected):
# @pytest.mark.parametrize('value, expected', (
#     [None, None],
#     ['\'foo\'', 'foo'],
#     ['"foo"', 'foo'],
#     ['`foo`', 'foo']))
    assert utils.remove_quotes(value) == expected
