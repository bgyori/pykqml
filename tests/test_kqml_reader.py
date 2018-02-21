import sys
from io import BytesIO
from kqml import KQMLObject
from kqml.kqml_reader import KQMLReader
from kqml.kqml_list import KQMLList

def test_read_list():
    s = b'(FAILURE :reason INVALID_DESCRIPTION)'
    sreader = BytesIO(s)
    kr = KQMLReader(sreader)
    lst = kr.read_list()
    for obj in lst:
        assert isinstance(obj, KQMLObject)

def test_read_performative():
    s = b'(REQUEST :CONTENT (REQUEST_TYPE :CONTENT "<ekb>ONT::PROTEIN</ekb>"))'
    sreader = BytesIO(s)
    kr = KQMLReader(sreader)
    kp = kr.read_performative()

def test_read_performative_utf8():
    s = '(REQUEST :CONTENT (REQUEST_TYPE :CONTENT "<ekb>\U0001F4A9</ekb>"))'
    s = s.encode('utf-8')
    sreader = BytesIO(s)
    kr = KQMLReader(sreader)
    kp = kr.read_performative()
