from kqml import KQMLObject
from kqml.kqml_list import KQMLList
from kqml.kqml_token import KQMLToken

def test_init():
    kl = KQMLList()
    assert(kl.data == [])
    kl = KQMLList('head')
    assert(kl.data == ['head'])
    assert(type(kl.data[0] == KQMLToken))
    kl = KQMLList(['a', 'b'])
    assert(kl.data == ['a', 'b'])

def test_from_string():
    s = b'(FAILURE :reason INVALID_DESCRIPTION)'
    kl = KQMLList.from_string(s)
    for obj in kl.data:
        assert(isinstance(obj, KQMLObject))

def test_gets():
    kl = KQMLList.from_string(b'(:hello "")')
    hello = kl.gets('hello')
    assert(hello == '')
