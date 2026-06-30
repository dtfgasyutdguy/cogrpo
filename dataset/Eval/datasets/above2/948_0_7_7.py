# -*- coding: utf-8 -*-
import hashlib

#     hasher = hashlib.md5()

def compute_md5(file_bytes):

    hasher.update(file_bytes)
    return hasher.hexdigest().upper()


def compute_sha256(input_string):
    hasher = hashlib.sha256()

    input_bytes = input_string.encode('utf-8')
    hasher.update(input_bytes)
    return hasher.hexdigest()
