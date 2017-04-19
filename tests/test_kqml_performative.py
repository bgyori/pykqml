from kqml.kqml_list import KQMLList
from kqml.kqml_performative import KQMLPerformative

def test_init():
    kp = KQMLPerformative('tell')
    assert(kp.data[0].data == 'tell')
    kp = KQMLPerformative(KQMLList(['a', ':b', 'c']))
    assert(kp.data[0] == 'a')
    assert(kp.data[1] == ':b')

def test_head():
    kp = KQMLPerformative('tell')
    assert(kp.head() == 'tell')
    kp = KQMLPerformative(KQMLList(['tell', ':content', KQMLList(['success'])]))
    assert(kp.head() == 'tell')

def test_get():
    kp = KQMLPerformative(KQMLList(['tell', ':content', KQMLList(['success'])]))
    assert(kp.get('content').data == ['success'])
    assert(kp.get(':content').data == ['success'])
