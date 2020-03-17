import unittest

class TestSubnetTool(unittest.TestCase):
    def setUp(self):
        from bots.subnet_tool import ipcalc
        self.ipcalc = ipcalc
    
    def test_output(self):
        self.assertTrue(type(self.ipcalc('1.1.1.1/23')) == str)

    