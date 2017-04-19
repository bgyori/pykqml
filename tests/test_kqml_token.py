from kqml.kqml_token import KQMLToken

def test_init():
    kt = KQMLToken('token')
    assert(kt.data == 'token')
    kt = KQMLToken()
    assert(kt.data == '')

def test_len():
    kt = KQMLToken('token')
    assert(len(kt) == 5)

def test_package():
    kt = KQMLToken('ONT::TOKEN')
    package, bare = kt.parse_package()
    assert(package == 'ONT')
    assert(bare == 'TOKEN')
    assert(kt.has_package())
    kt = KQMLToken('ONT::|TOKEN|')
    package, bare = kt.parse_package()
    assert(package == 'ONT')
    assert(bare == '|TOKEN|')
    assert(kt.has_package())
    kt = KQMLToken('ONT::|TOK::EN|')
    package, bare = kt.parse_package()
    assert(package == 'ONT')
    assert(bare == '|TOK::EN|')
    assert(kt.has_package())
    kt = KQMLToken(':keyword')
    package, bare = kt.parse_package()
    assert(package == None)
    assert(bare == ':keyword')
    assert(not kt.has_package())

def test_is_keyword():
    kt = KQMLToken(':keyword')
    assert(kt.is_keyword())
    kt = KQMLToken('token')
    assert(not kt.is_keyword())
    kt = KQMLToken('ONT::TOKEN')
    assert(not kt.is_keyword())

def test_equals():
    assert(KQMLToken('token') == 'token')
    assert(KQMLToken('token') != 'token1')
    assert(KQMLToken('token') == KQMLToken('token'))
    assert(KQMLToken('token') != KQMLToken('token1'))
    assert(KQMLToken('token').equals_ignore_case('TOKEN'))
    assert(KQMLToken('token').equals_ignore_case(KQMLToken('TOKEN')))
