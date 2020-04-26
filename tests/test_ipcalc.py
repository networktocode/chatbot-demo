import unittest

class TestIpcalcTool(unittest.TestCase):
    def setUp(self):
        from lib.ipcalc import ipcalc

        self.ipcalc = ipcalc

    def test_output(self):
        self.assertTrue(type(self.ipcalc("1.1.1.1/23")) == str)
