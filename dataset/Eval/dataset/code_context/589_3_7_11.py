# -*- coding: utf-8 -*-
import pytest

from tests.test_all import compare_strings



def test_strict_variable_comparison(gold, pred, strict, expected):
    assert (
        compare_strings(gold, pred, match_types=["latex", "expr"], strict=strict)
        == expected
    )
