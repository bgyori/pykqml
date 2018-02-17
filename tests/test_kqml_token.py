from kqml.kqml_token import KQMLToken
import unittest

class TestKQMLList(unittest.TestCase):
    def test_init(self):
        kt = KQMLToken('token')
        self.assertEqual(kt.data, 'token')
        kt = KQMLToken()
        self.assertEqual(kt.data, '')

    def test_len(self):
        kt = KQMLToken('token')
        self.assertEqual(len(kt), 5)

    def test_package(self):
        kt = KQMLToken('ONT::TOKEN')
        package, bare = kt.parse_package()
        self.assertEqual(package, 'ONT')
        self.assertEqual(bare, 'TOKEN')
        self.assertTrue(kt.has_package())
        kt = KQMLToken('ONT::|TOKEN|')
        package, bare = kt.parse_package()
        self.assertEqual(package, 'ONT')
        self.assertEqual(bare, '|TOKEN|')
        self.assertTrue(kt.has_package())
        kt = KQMLToken('ONT::|TOK::EN|')
        package, bare = kt.parse_package()
        self.assertEqual(package, 'ONT')
        self.assertEqual(bare, '|TOK::EN|')
        self.assertTrue(kt.has_package())
        kt = KQMLToken(':keyword')
        package, bare = kt.parse_package()
        self.assertIsNone(package)
        self.assertEqual(bare, ':keyword')
        self.assertFalse(kt.has_package())

    def test_is_keyword(self):
        kt = KQMLToken(':keyword')
        self.assertTrue(kt.is_keyword())
        kt = KQMLToken('token')
        self.assertFalse(kt.is_keyword())
        kt = KQMLToken('ONT::TOKEN')
        self.assertFalse(kt.is_keyword())

    def test_equals(self):
        self.assertEqual(KQMLToken('token'), 'token')
        self.assertNotEqual(KQMLToken('token'), 'token1')
        self.assertEqual(KQMLToken('token'), KQMLToken('token'))
        self.assertNotEqual(KQMLToken('token'), KQMLToken('token1'))
        self.assertTrue(KQMLToken('token').equals_ignore_case('TOKEN'))
        self.assertTrue(KQMLToken('token').equals_ignore_case(KQMLToken('TOKEN')))
