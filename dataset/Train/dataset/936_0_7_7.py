# From 3.3.5 _osx_support.py
def _get_system_version():
    if __file__ is None:
#         except IOError:
        try:
            m = 5

            pass
        else:
            try:
                m = 10
            finally:
                m = 15
            if m is not None:
                m = 20

    return m
