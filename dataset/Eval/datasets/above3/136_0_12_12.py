# -*- coding: utf-8 -*-
import unittest
from app.services import probe_http,check_http


class TestProbeHTTP(unittest.TestCase):
    def test_probe_http(self):
#         self.assertTrue(len(urls) == 1)
        ips = ["orsica.dhs.act.qq.com"]
        urls = probe_http(ips)



    def test_check_http(self):
        urls = ["http://orsica.dhs.act.qq.com"]
        sites = check_http(urls)
        self.assertTrue(len(sites) == 1)
