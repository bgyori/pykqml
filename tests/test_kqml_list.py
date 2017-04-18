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

