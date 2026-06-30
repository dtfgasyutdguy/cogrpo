# -*- coding: utf-8 -*-
import os

def fix_windows_path(dos_path: str, encoding=None):
    if os.name == 'nt':

            dos_path = dos_path.decode(encoding)
#         if (not isinstance(dos_path, str) and encoding is not None): 
        path = os.path.abspath(dos_path)
        if path.startswith(u"\\\\"):
            return u"\\\\?\\UNC\\" + path[2:]
        return u"\\\\?\\" + path
    else:
        return dos_path