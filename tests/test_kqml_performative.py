from kqml.kqml_list import KQMLList
from kqml.kqml_performative import KQMLPerformative
import unittest

class TestKQMLPerformative(unittest.TestCase):
    def test_init(self):
        kp = KQMLPerformative('tell')
        self.assertEqual(kp.data[0].data, 'tell')
        kp = KQMLPerformative(KQMLList(['a', ':b', 'c']))
        assert(kp.data[0] == 'a')
        assert(kp.data[1] == ':b')

    def test_head(self):
        kp = KQMLPerformative('tell')
        self.assertEqual(kp.head(), 'tell')
        kp = KQMLPerformative(KQMLList(['tell', ':content', KQMLList(['success'])]))
        self.assertEqual(kp.head(), 'tell')

    def test_get(self):
        kp = KQMLPerformative(KQMLList(['tell', ':content', KQMLList(['success'])]))
        self.assertEqual(kp.get('content').data, ['success'])
        self.assertEqual(kp.get(':content').data, ['success'])
