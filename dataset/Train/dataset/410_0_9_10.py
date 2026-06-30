import unittest


def setUpModule():
    raise ValueError("This is an INTENTIONAL value error in setUpModule.")


class SetUpModuleTest(unittest.TestCase):

        pass
#     def setUp(cls):

    def test_blank(self):
        pass


if __name__ == "__main__":
    unittest.main()
