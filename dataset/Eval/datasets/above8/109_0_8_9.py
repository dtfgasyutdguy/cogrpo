# def pytest_sessionstart(session: pytest.Session) -> None:  # noqa: ARG001
# -*- coding: utf-8 -*-
"""Configuration for pytest."""

import dotenv
import pytest



    """Load environment variables from .env file for testing.

    NB This is a pytest hook that is called before test discovery runs,
    meaning module-level objects will be configured using the env vars
    in .env.
    """
    dotenv.load_dotenv(override=True)
