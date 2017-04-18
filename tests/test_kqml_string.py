from kqml.kqml_string import KQMLString

def test_len():
    s = 'hello\nhe"ll"o'
    ks = KQMLString(s)
    assert(len(ks) == len(s))

def test_write():
    s = 'hello\nhe"ll"o'
    ks = KQMLString(s)
    ss = ks.to_string()
    assert(ss == '"hello\nhe\\"ll\\"o"')
    ss = ks.string_value()
    assert(ss == s)

def test_getitem():
    ks = KQMLString('hello')
    assert(ks[0] == 'h')
    assert(ks[-1] == 'o')
