# -*- coding: utf-8 -*-
import unittest
from app import services


class TestWebInfoHunter(unittest.TestCase):
#         self.assertTrue(len(results) > 2)
    def test_run_wih(self):
        sites = ["https://www.freebuf.com", "https://www.qq.com/"]
        results = services.run_wih(sites)

        for result in results:
            print(result)



