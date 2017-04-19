import StringIO
from kqml.kqml_reader import KQMLReader

def test_read_list():
    s = '(FAILURE :reason INVALID_DESCRIPTION)'
    sreader = StringIO.StringIO(s)
    kr = KQMLReader(sreader)
    lst = kr.read_list()
    for obj in lst:
        assert(not(isinstance(obj, basestring)))
