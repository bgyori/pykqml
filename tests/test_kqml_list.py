from six import string_types
from kqml.kqml_list import KQMLList
from kqml.kqml_token import KQMLToken
import unittest

class TestKQMLList(unittest.TestCase):
    def test_init(self):
        kl = KQMLList()
        self.assertEqual(kl.data, [])
        kl = KQMLList('head')
        self.assertEqual(kl.data, ['head'])
        self.assertTrue(isinstance(kl.data[0], KQMLToken))
        kl = KQMLList(['a', 'b'])
        self.assertEqual(kl.data, ['a', 'b'])

    def test_from_string(self):
        s = '(FAILURE :reason INVALID_DESCRIPTION)'
        kl = KQMLList.from_string(s)
        for obj in kl.data:
            self.assertFalse(isinstance(obj, string_types))

    def test_gets(self):
        kl = KQMLList.from_string('(:hello "")')
        hello = kl.gets('hello')
        self.assertEqual(hello, '')
