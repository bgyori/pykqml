from kqml import KQMLModule
import unittest

class TestKQMLModule(unittest.TestCase):
    def test_init(self):
        """Tests whether KQMLModule can be initialized."""
        KQMLModule(testing=True, name='testmodule')
