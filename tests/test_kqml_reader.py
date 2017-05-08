import sys
import StringIO
from kqml.kqml_reader import KQMLReader
from kqml.kqml_list import KQMLList

def test_read_list():
    s = '(FAILURE :reason INVALID_DESCRIPTION)'
    sreader = StringIO.StringIO(s)
    kr = KQMLReader(sreader)
    lst = kr.read_list()
    for obj in lst:
        assert(not(isinstance(obj, basestring)))

def test_read_performative():
    s = '(REQUEST :CONTENT (REQUEST_TYPE :CONTENT "<ekb>ONT::PROTEIN</ekb>"))'
    sreader = StringIO.StringIO(s)
    kr = KQMLReader(sreader)
    kp = kr.read_performative()
