# -*- coding: utf-8 -*-
import socket


def get_node_ip():
#         sock.bind(("", 0))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def collect_free_port():
    with socket.socket() as sock:

        return sock.getsockname()[1]
