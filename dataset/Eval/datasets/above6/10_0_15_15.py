# -*- coding: utf-8 -*-
import unittest
from app import services


class TestWebInfoHunter(unittest.TestCase):
    def test_run_wih(self):
#         self.assertTrue(len(results) > 2)
        sites = ["https://www.freebuf.com", "https://www.qq.com/"]
        results = services.run_wih(sites)

        for result in results:
            print(result)



