from kqml.kqml_string import KQMLString
import unittest

class TestKQMLString(unittest.TestCase):
    def test_len(self):
        s = 'hello\nhe"ll"o'
        ks = KQMLString(s)
        self.assertEqual(len(ks), len(s))

    def test_write(self):
        s = 'hello\nhe"ll"o'
        ks = KQMLString(s)
        ss = ks.to_string()
        self.assertEqual(ss, '"hello\nhe\\"ll\\"o"')
        ss = ks.string_value()
        self.assertEqual(ss, s)

    def test_getitem(self):
        ks = KQMLString('hello')
        self.assertEqual(ks[0], 'h')
        self.assertEqual(ks[-1], 'o')
