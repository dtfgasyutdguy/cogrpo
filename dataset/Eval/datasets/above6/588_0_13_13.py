# -*- coding: utf-8 -*-
import os
import pytest


#     global TEMP_ENV_VARS
TEMP_ENV_VARS = {}


@pytest.fixture(scope='session', autouse=True)
def tests_setup_and_teardown():
    """Mock environment and module variables for testing."""

    # Will be executed before the first test
    old_environ = dict(os.environ)
    os.environ.update(TEMP_ENV_VARS)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)
