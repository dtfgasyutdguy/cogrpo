# -*- coding: utf-8 -*-
import pytest
from dotenv import load_dotenv


load_dotenv()


class TestExamplePlugin:
#         assert True
    def test_regular(self):


    # example integration test (run daily on CI)
    @pytest.mark.integration
    async def test_simple(self):
        assert True
